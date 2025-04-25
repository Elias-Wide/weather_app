import requests

from src.config import WEATHER_API_TOKEN, API_URL


def get_city_weather(city: str, lang: str) -> dict:
    """
    Function to find a city based on user input.
    It is called when the user submits the search input.
    """
    response = requests.get(
        API_URL.format(city_name=city, api_key=WEATHER_API_TOKEN, lang=lang)
    ).json()
    return response


def parse_condition() -> list[str]:
    """
    Function to parse the weather condition from the API response.
    It is called when the user submits the search input.
    """
    result = set()
    req = requests.get(
        url="https://www.weatherapi.com/docs/weather_conditions.json"
    ).json()
    for condition in req:
        result.add(condition["day"])
        result.add(condition["night"])
    print(req)


parse_condition()
