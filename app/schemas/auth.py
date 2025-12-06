from pydantic import BaseModel, EmailStr, field_validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        if v is None:
            return v
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Password must not be empty")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    @field_validator("access_token")
    @classmethod
    def validate_access_token(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("access_token must not be empty")
        return v

    @field_validator("token_type")
    @classmethod
    def validate_token_type(cls, v: str) -> str:
        v = v.strip().lower()
        if v != "bearer":
            raise ValueError("token_type must be 'bearer'")
        return v
