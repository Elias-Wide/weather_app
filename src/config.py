from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="main.env", env_file_encoding="utf-8", extra="ignore"
    )
    weather_api_token: str
    api_url: str
    app_name: str
    app_version: str
    ip_info_token: str
    default_lang: str


settings = Settings()
