from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator


class UserBase(BaseModel):
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        if v is None:
            return v
        return v.strip().lower()


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        v = v.strip()

        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")

        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")

        if not any(not c.isalnum() for c in v):
            raise ValueError("Password must contain at least one special character")

        return v


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
