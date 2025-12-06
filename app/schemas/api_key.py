from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator


class ApiKeyCreate(BaseModel):
    label: Optional[str] = None
    expires_in_days: Optional[int] = None

    @field_validator("label")
    @classmethod
    def normalize_label(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if len(v) > 50:
            raise ValueError("Label must be at most 50 characters long")
        return v

    @field_validator("expires_in_days")
    @classmethod
    def validate_expires_in_days(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return 30  # Default to 30 days
        if v <= 0:
            raise ValueError("expires_in_days must be a positive integer")
        if v > 365:
            raise ValueError("expires_in_days cannot be more than 365 days")
        return v


class ApiKeyRead(BaseModel):
    id: int
    label: Optional[str]
    created_at: datetime
    expires_at: Optional[datetime]
    revoked: bool

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def validate_dates(self) -> "ApiKeyRead":
        if self.expires_at and self.expires_at < self.created_at:
            raise ValueError("expires_at cannot be before created_at")
        return self


class ApiKeyPlain(BaseModel):
    """
    Response when a key is first created.
    We return the plain key only once.
    """

    api_key: str
    label: Optional[str]
    expires_at: Optional[datetime]

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("api_key must not be empty")
        return v

    @field_validator("label")
    @classmethod
    def normalize_label(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if len(v) > 50:
            raise ValueError("Label must be at most 50 characters long")
        return v
