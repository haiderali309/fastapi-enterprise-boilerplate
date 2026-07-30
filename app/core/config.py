from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME : str
    DEBUG : bool = True
    DATABASE_URL : str
    BASE_URL : str
    ALLOWED_HOSTS : str
    CORS_ORIGINS : str
    ENABLE_HTTPS_REDIRECT : bool = False
    JWT_SECRET : str
    JWT_ALGO : str
    ACCESS_TOKEN_EXPIRY_MINUTE : int


    model_config=SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )


settings=Settings()
