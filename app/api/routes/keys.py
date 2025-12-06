from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep, get_current_user
from app.core.security import generate_api_key, hash_api_key
from app.models.api_key import ApiKey
from app.models.user import User
from app.schemas.api_key import ApiKeyCreate, ApiKeyRead, ApiKeyPlain

router = APIRouter(prefix="/keys", tags=["API Keys"])


@router.post("/create", response_model=ApiKeyPlain, status_code=status.HTTP_201_CREATED)
def create_api_key(
    payload: ApiKeyCreate,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
) -> ApiKeyPlain:
    raw_key = generate_api_key(prefix="svc")
    key_hash = hash_api_key(raw_key)

    expires_at = None
    if payload.expires_in_days is not None and payload.expires_in_days > 0:
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=payload.expires_in_days
        )

    api_key = ApiKey(
        key_hash=key_hash,
        label=payload.label,
        owner_user_id=current_user.id,
        expires_at=expires_at,
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return ApiKeyPlain(
        api_key=raw_key,
        label=api_key.label,
        expires_at=api_key.expires_at,
    )


@router.get("/", response_model=List[ApiKeyRead])
def list_api_keys(
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
) -> list[ApiKey]:
    keys = (
        db.query(ApiKey)
        .filter(ApiKey.owner_user_id == current_user.id)
        .order_by(ApiKey.created_at.desc())
        .all()
    )
    return keys


@router.post("/{key_id}/revoke", response_model=ApiKeyRead)
def revoke_api_key(
    key_id: int,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
) -> ApiKey:
    api_key = (
        db.query(ApiKey)
        .filter(
            ApiKey.id == key_id,
            ApiKey.owner_user_id == current_user.id,
        )
        .first()
    )
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )

    if api_key.revoked:
        return api_key

    api_key.revoked = True
    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return api_key
