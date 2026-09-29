from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application Settings powered by Pydantic BaseSettings.
    Automatically loads and validates configuration parameters from `.env`.
    """
    # Core Application Settings
    APP_NAME: Optional[str] = "FastAPI Enterprise"
    DEBUG: bool = True

    # Database & Networking
    DATABASE_URL: Optional[str] = None
    BASE_URL: Optional[str] = None
    FRONTEND_URL: Optional[str] = None

    # Security & CORS
    ALLOWED_HOSTS: Optional[str] = "localhost,127.0.0.1"
    CORS_ORIGINS: Optional[str] = "http://localhost:3000"
    ENABLE_HTTPS_REDIRECT: bool = False

    # JWT Authentication & Expirations
    JWT_SECRET: Optional[str] = None
    JWT_ALGO: Optional[str] = "HS256"
    ACCESS_TOKEN_EXPIRY_MINUTE: Optional[int] = 30
    REFRESH_TOKEN_EXPIRY_DAYS: Optional[int] = 30
    EMAIL_VERIFY_TOKEN_EXPIRY_MINUTE: Optional[int] = 15
    PASSWORD_RESET_EXPIRY_MINUTE: Optional[int] = 10

    # Email Infrastructure Settings
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: Optional[int] = 587
    MAIL_SERVER: Optional[str] = "smtp.gmail.com"
    MAIL_STARTTLS: Optional[bool] = True
    MAIL_SSL_TLS: Optional[bool] = False
    USE_CREDENTIALS: Optional[bool] = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Instantiate settings object globally
settings = Settings()
