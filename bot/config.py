"""Bot konfiguratsiyasi — .env fayldan o'qish (pydantic-settings)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BOT_TOKEN: str
    WEBAPP_URL: str = "https://maktabos370.lovable.app/scan"
    API_BASE_URL: str
    BOT_API_SECRET: str


settings = Settings()
