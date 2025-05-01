from datetime import datetime
import requests

from src.config import settings
from src.database.dao import WeatherConditionsDAO


def get_conditions_from_api() -> list[dict[str]]:
    """
    Fetches weather conditions from the Weather API.

    Returns:
        list[dict[str]]: A list of dictionaries containing weather condition codes,
        day descriptions, and night descriptions.
    """
    response = requests.get(
        url="https://www.weatherapi.com/docs/weather_conditions.json"
    ).json()
    return list(
        map(
            lambda c: {
                "code": c["code"],
                "day": c["day"],
                "night": c["night"],
            },
            response,
        )
    )


def insert_weather_conditions_data(weather_conditions: list[dict]):
    """
    Inserts weather condition data into the database.

    Args:
        weather_conditions (list[dict]): A list of dictionaries containing weather condition data.
    """
    for data in weather_conditions:
        WeatherConditionsDAO.create(data)


def get_city_weather(city: str) -> dict:
    """
    Fetches weather data for a specific city from the Weather API.

    Args:
        city (str): The name of the city.
        lang (str): The language code for the API response.

    Returns:
        dict: A dictionary containing weather data for the city, including temperature,
        condition, wind speed, humidity, and more. Returns None if the API request fails.
    """
    response = requests.get(
        settings.api_url.format(
            api_key=settings.weather_api_token,
            city=city,
        )
    )
    if response.status_code != 200:
        return None
    print(response.json())
    return response.json()
