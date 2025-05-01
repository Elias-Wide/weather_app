from datetime import datetime

from src.constants import DEFAULT_ICON_SRC
from src.database.dao import WeatherConditionsDAO


class CityWeather:
    """
    A class representing weather data for a city.
    Initializes attributes based on the keys in the response dictionary.
    """

    def __init__(self, response_dict: dict):
        location = response_dict.get("location", {})
        self._name = location.get("name", "Unknown")
        self._country = location.get("country", "Unknown")
        self.localtime = location.get(
            "localtime", datetime.now().strftime("%A, %d %B, %H:%M")
        )
        self._lat = location.get("lat", 0.0)
        self._lon = location.get("lon", 0.0)

        current = response_dict.get("current", {})
        self._temp_c = current.get("temp_c", 0.0)
        self._wind_kph = current.get("wind_kph", 0.0)
        self._wind_dir = current.get("wind_dir", "Unknown")
        self._humidity = current.get("humidity", 0)
        self.condition_code = current.get("condition", {}).get("code", 1000)
        self.icon_src = current.get("condition", {}).get(
            "icon", DEFAULT_ICON_SRC
        )
        self.is_day = current.get("is_day", 0)
        self.condition = self.get_condition_text()

    @property
    def name(self):
        return self._name.capitalize()

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def country(self):
        return self._country.capitalize()

    @country.setter
    def country(self, value):
        self._country = value

    @property
    def temp_c(self):
        return self._temp_c

    @temp_c.setter
    def temp_c(self, value):
        self._temp_c = value

    def formatted_temp_c(self):
        return f"{self._temp_c}°C"

    @property
    def wind_kph(self):
        return self._wind_kph

    @wind_kph.setter
    def wind_kph(self, value):
        self._wind_kph = value

    def get_condition_text(self):
        condition = WeatherConditionsDAO.get_condition_by_code(
            self.condition_code
        )
        if not self.is_day:
            return condition["night"]
        return condition["day"]

    def formatted_wind_kph(self):
        return f"Wind: {self._wind_kph}kp/h"

    def get_city_date(self):
        try:
            city_dt = datetime.strptime(self.localtime, "%Y-%m-%d %H:%M")
            return city_dt.strftime("%A, %d %B, %H:%M")
        except ValueError:
            return datetime.now().strftime("%A, %d %B, %H:%M")

    def __repr__(self):
        return (
            f"CityWeather(name={self._name}, country={self._country}, "
            f"temp_c={self._temp_c}, wind_kph={self._wind_kph})"
        )

    def get_weather_data(self):
        return (
            self.icon_src,
            self.name,
            self.get_city_date(),
            self.condition,
            self.temp_c,
            self.wind_kph,
            self._humidity,
        )
