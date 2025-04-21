import requests

from src.config import API_KEY, API_URL


def get_city_weather(city: str, lang: str) -> dict:
    """
    Function to find a city based on user input.
    It is called when the user submits the search input.
    """
    response = requests.get(
        API_URL.format(city_name=city, api_key=API_KEY, lang=lang)
    ).json()
    print(response, type(response))
