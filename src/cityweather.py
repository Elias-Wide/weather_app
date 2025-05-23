from datetime import datetime
from typing import Optional, Dict

from localizations import localize_city_name
from parse_api import get_weather_icon
from src.constants import DEFAULT_ICON_SRC
from localizations import HUMIDITY, WIND, weather_conditions


class CityWeather:
    """
    A class representing weather data for a city.
    Initializes attributes based on the keys in the response dictionary.
    """

    def __init__(self, response_dict: Dict, lang: str = "en") -> None:
        """
        Initializes the CityWeather object.

        Args:
            response_dict (dict): The dictionary containing weather data for the city.
            lang (str): The language code for localization (default is "en").
        """
        self.lang: str = lang
        location: dict = response_dict.get("location", {})
        self.name: str = location.get("name", "Unknown")
        self.country: str = location.get("country", "Unknown")
        self.region: str = location.get("region", "Unknown")
        localtime_str: Optional[str] = location.get("localtime")
        if localtime_str:
            try:
                self.localtime: datetime = datetime.strptime(
                    localtime_str, "%Y-%m-%d %H:%M"
                )
            except ValueError:
                self.localtime: datetime = datetime.now()
        else:
            self.localtime: datetime = datetime.now()
        self.lat: str = str(location.get("lat", 0.0))
        self.lon: str = str(location.get("lon", 0.0))

        current: dict = response_dict.get("current", {})
        self.is_day: int = current.get("is_day", 0)
        self._temp_c: float = current.get("temp_c", 0.0)
        self._wind_kph: float = current.get("wind_kph", 0.0)
        self._wind_dir: str = current.get("wind_dir", "Unknown")
        self.humidity: int = current.get("humidity", 0)
        self.condition_code: int = current.get("condition", {}).get(
            "code", 1000
        )
        self.icon_src: str = "https:" + current.get("condition", {}).get(
            "icon", DEFAULT_ICON_SRC
        )

    @property
    def name(self) -> str:
        """
        Returns the capitalized name of the city.
        """
        return self._name.capitalize()

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def country(self) -> str:
        """
        Returns the capitalized name of the country.
        """
        return self._country.capitalize()

    @country.setter
    def country(self, value: str) -> None:
        self._country = value

    @property
    def icon_path(self) -> str:
        """
        Returns the local path to the weather icon.
        """
        return get_weather_icon(self.get_icon_name(), self.icon_src)

    @property
    def condition_code(self) -> int:
        """
        Returns the condition code for the weather.
        """
        return self._condition_code

    @condition_code.setter
    def condition_code(self, value: int) -> None:
        if value == 1000 and not self.is_day:
            value += 1
        self._condition_code = value

    @property
    def temp_c(self) -> float:
        """
        Returns the temperature in Celsius.
        """
        return self._temp_c

    @temp_c.setter
    def temp_c(self, value: float) -> None:
        self._temp_c = value

    def formatted_temp_c(self) -> str:
        """
        Returns the formatted temperature in Celsius as a string.
        """
        return f"{self._temp_c}°C"

    @property
    def wind_kph(self) -> float:
        """
        Returns the wind speed in kilometers per hour.
        """
        return self._wind_kph

    @wind_kph.setter
    def wind_kph(self, value: float) -> None:
        self._wind_kph = value

    def get_formatted_name(self) -> str:
        """
        Returns the localized and capitalized name of the city.
        """
        return localize_city_name(self.name, self.lang).capitalize()

    def get_condition_text(self) -> str:
        """
        Returns the localized text description of the weather condition.
        """
        return weather_conditions[self.condition_code][self.lang]

    def formatted_wind_kph(self) -> str:
        """
        Returns the formatted wind speed as a string.
        """
        return WIND[self.lang].format(self._wind_kph)

    def formatted_humidity(self) -> str:
        """
        Returns the formatted humidity as a string.
        """
        return HUMIDITY[self.lang].format(self.humidity)

    def get_city_local_time(self) -> str:
        """
        Returns the formatted local time for the city as a string (HH:MM).
        """
        return self.localtime.strftime("%H:%M")

    def get_city_date(self) -> str:
        """
        Returns the formatted local date and time for the city.

        For English: e.g., "Saturday, 18 May, 00:40"
        For Russian: e.g., "Суббота, 18 Мая, 00:40"
        """
        city_dt = self.localtime
        if self.lang == "ru":
            days = [
                "Понедельник",
                "Вторник",
                "Среда",
                "Четверг",
                "Пятница",
                "Суббота",
                "Воскресенье",
            ]
            months = [
                "",
                "Января",
                "Февраля",
                "Марта",
                "Апреля",
                "Мая",
                "Июня",
                "Июля",
                "Августа",
                "Сентября",
                "Октября",
                "Ноября",
                "Декабря",
            ]
            weekday = days[city_dt.weekday()]
            month = months[city_dt.month]
            return f"{weekday}, {city_dt.day} {month}, {city_dt.strftime(u'%H:%M')}"
        return city_dt.strftime("%A, %d %B, %H:%M")

    def __repr__(self) -> str:
        """
        Returns a string representation of the CityWeather object.
        """
        return (
            f"CityWeather(name={self._name}, country={self._country}, "
            f"temp_c={self._temp_c}, wind_kph={self._wind_kph})"
        )

    def get_icon_name(self) -> str:
        """
        Returns the name of the weather icon file based on the condition code and day/night status.
        """
        return f"{self.condition_code}_{self.is_day}.png"

    def get_weather_data(self) -> tuple:
        """
        Returns a tuple containing detailed weather data for the city.
        """
        return (
            self.name,
            self.get_city_date(),
            self.get_condition_text(),
            self.temp_c,
            self.wind_kph,
            self.humidity,
        )

    def get_weather_data_small(self) -> tuple:
        """
        Returns a tuple containing basic weather data for the city.
        """
        return (
            self.name,
            self.get_city_date(),
            self.condition_code,
            self.temp_c,
        )

    def formated_data_for_favs(self) -> dict:
        """
        Returns a dictionary containing formatted data for saving the city to favorites.
        """
        return {
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
        }
