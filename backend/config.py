import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_env: str = Field("development", env="APP_ENV")
    app_port: int = Field(8080, env="APP_PORT")
    app_url: str = Field("http://localhost:8080", env="APP_URL")

    db_host: str = Field("127.0.0.1", env="DB_HOST")
    db_port: int = Field(3306, env="DB_PORT")
    db_name: str = Field("endo_count", env="DB_NAME")
    db_user: str = Field("endo_user", env="DB_USER")
    db_password: str = Field("password", env="DB_PASSWORD")

    jwt_secret: str = Field("change_this", env="JWT_SECRET")
    jwt_expires_in: str = Field("12h", env="JWT_EXPIRES_IN")

    cors_allowed_origins: str = Field("http://localhost:3000", env="CORS_ALLOWED_ORIGINS")

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        env_file_encoding = "utf-8"


settings = Settings()
