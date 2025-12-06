from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_NAME: str = "HNG Stage 7 - Task 3"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    APP_PORT: int = 8000

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/mini_auth_api_key_db"

    # JWT
    JWT_SECRET_KEY: str = "change-this-in-env"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
