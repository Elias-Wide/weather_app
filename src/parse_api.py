import datetime
import os
import requests
from cachetools import cached, TTLCache
from constants import WEATHER_ICONS_PATH
from src.config import settings

city_weather_cache = TTLCache(maxsize=100, ttl=600)


def get_conditions_from_api() -> list[dict[str]]:
    """
    Fetches weather conditions from the Weather API.

    Returns:
        list[dict[str]]: A list of dictionaries containing weather condition codes,
        day descriptions, and night descriptions.

    Used during development to collect data for displaying text in localizations.py.
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


@cached(city_weather_cache)
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
    return response.json()


def get_weather_icon(icon_name: str, icon_src: str):
    icon_path = find_file_in_directory(icon_name, WEATHER_ICONS_PATH)
    if not icon_path:
        download_weather_icon(icon_src, icon_name)
    return find_file_in_directory(icon_name, WEATHER_ICONS_PATH)


def download_weather_icon(url: str, icon_name: str) -> None:
    """
    Downloads an image from the given URL and saves it to the specified path.

    Args:
        url (str): The URL of the image to download.
        icon_name (str): file_name for the image will be saved.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(WEATHER_ICONS_PATH + icon_name, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")


def find_file_in_directory(file_name: str, directory: str) -> str | None:
    """
    Searches for a file by name in the specified directory.

    Args:
        file_name (str): The name of the file to search for.
        directory (str): The directory to search in.

    Returns:
        str | None: The full path to the file if found, otherwise None.
    """
    for root, _, files in os.walk(directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return None


def get_time_difference(
    request_time: datetime.datetime, response_time: datetime.datetime
) -> float:
    """
    Calculates the time difference in seconds between the request and the response from the database.

    Args:
        request_time (datetime.datetime): The time when the request was made.
        response_time (datetime.datetime): The time when the response was received from the database.

    Returns:
        float: The time difference in seconds.
    """
    return (response_time - request_time).total_seconds()


def read_file(file_path: str) -> str:
    """
    Reads the first line from a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The first line of the file as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readline().strip()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
