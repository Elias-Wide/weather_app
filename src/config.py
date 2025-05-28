import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from get_api_key import read_file

# Определение пути к рабочей директории
WORKING_DIR = os.getcwd()

# Чтение API ключа из файла
file_path = os.path.join(WORKING_DIR, "weather_api.txt")
api_key = read_file(file_path)


class Settings(BaseSettings):
    """
    Configuration class for the application.
    Combines data from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=os.path.join(WORKING_DIR, "main.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )
    weather_api_token: str = api_key
    api_url: str = (
        "https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no&lang=eng"
    )
    app_name: str = "Weather App"
    app_version: str = "0.1.0"
    default_lang: str = "en"
    db_name: str = "app_db"


settings = Settings()
