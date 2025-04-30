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
    response = response.json()
    print(response)
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
    )  # CREATE DB REQUEST FOR GETTING CONDITION BY ITS CODE FROM API RESPONSE
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


response_dict = {
    "location": {
        "name": "Moscow",
        "region": "Moscow City",
        "country": "Russia",
        "lat": 55.7522,
        "lon": 37.6156,
        "tz_id": "Europe/Moscow",
        "localtime_epoch": 1746029643,
        "localtime": "2025-04-30 19:14",
    },
    "current": {
        "last_updated_epoch": 1746028800,
        "last_updated": "2025-04-30 19:00",
        "temp_c": 11.2,
        "temp_f": 52.2,
        "is_day": 1,
        "condition": {
            "text": "Cloudy",
            "icon": "//cdn.weatherapi.com/weather/64x64/day/119.png",
            "code": 1006,
        },
        "wind_mph": 6.0,
        "wind_kph": 9.7,
        "wind_degree": 6,
        "wind_dir": "N",
        "pressure_mb": 1013.0,
        "pressure_in": 29.91,
        "precip_mm": 0.0,
        "precip_in": 0.0,
        "humidity": 43,
        "cloud": 25,
        "feelslike_c": 10.1,
        "feelslike_f": 50.2,
        "windchill_c": 2.7,
        "windchill_f": 36.8,
        "heatindex_c": 5.0,
        "heatindex_f": 40.9,
        "dewpoint_c": -0.7,
        "dewpoint_f": 30.8,
        "vis_km": 10.0,
        "vis_miles": 6.0,
        "uv": 0.1,
        "gust_mph": 8.6,
        "gust_kph": 13.9,
    },
}
