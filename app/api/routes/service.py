from fastapi import APIRouter, Depends

from app.api.deps import get_current_service
from app.models.api_key import ApiKey

router = APIRouter(prefix="/service", tags=["Service-to-Service"])


@router.get("/ping")
def service_ping(api_key: ApiKey = Depends(get_current_service)):
    """
    Service-only endpoint.
    Requires: x-api-key: <plain api key>
    """
    return {
        "status": "ok",
        "service_label": api_key.label,
        "owner_user_id": api_key.owner_user_id,
        "api_key_id": api_key.id,
    }
