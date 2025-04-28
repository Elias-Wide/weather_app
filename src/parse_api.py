from datetime import datetime
import requests

from src.config import API_URL, WEATHER_API_TOKEN
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


def get_city_weather(city: str, lang: str) -> dict:
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
        API_URL.format(
            api_key=WEATHER_API_TOKEN,
            city=city,
        )
    )
    if response.status_code != 200:
        return None
    response = response.json()
    result_data = {
        "city": city,
        "lat": response["location"]["lat"],
        "lon": response["location"]["lon"],
        "datetime": response["location"]["localtime"],
        "temp": response["current"]["temp_c"],
        "condition": response["current"]["condition"]["code"],
        "wind_kph": response["current"]["wind_kph"],
        "wind_dir": response["current"]["wind_dir"],
        "humidity": response["current"]["humidity"],
    }
    return result_data


def get_weather_page_data(data: dict[str]):
    """
    Formats weather data for display on the weather page.

    Args:
        data (dict[str]): A dictionary containing weather data.

    Returns:
        list[str]: A list of formatted strings representing the weather data,
        including city name, date, condition, temperature, wind speed, and humidity.
    """
    result = []
    result.append(data["city"].capitalize())
    result.append(get_city_date(data["datetime"]))
    result.append(
        data["condition"]
    )  # CREATE DB REQUEST FOR GETTING CONDITION BY IYS CODE FROM API RESPONSE
    result.append(f"{data['temp']}°C")
    result.append(f"Wind: {data["wind_kph"]}")
    result.append(f"Humidity: {data["humidity"]}%")
    return result


# city_data = {
#             "city": "moscow",
#             "lat": 55.7522,
#             "lon": 37.6156,
#             "datetime": "2025-04-28 23:01",
#             "temp": 7.1,
#             "condition": 1009,
#             "wind_kph": 13.3,
#             "wind_dir": "WSW",
#             "humidity": 45,
#         }
#         print(get_weather_page_data(city_data))


def get_city_date(city_dt: str):
    """
    Converts a date string into a formatted string with the day of the week.

    Args:
        city_dt (str): A date string in the format "YYYY-MM-DD HH:MM".

    Returns:
        str: A formatted string representing the date, including the day of the week,
        day, month, and time (e.g., "Monday, 28 April, 23:01").
    """
    city_dt = datetime.strptime(city_dt, "%Y-%m-%d %H:%M")
    return city_dt.strftime("%A, %d %B, %H:%M")
