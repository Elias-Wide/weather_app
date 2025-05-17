from datetime import datetime
import locale

from localizations import localize_city_name
from parse_api import get_weather_icon
from src.constants import DEFAULT_ICON_SRC
from localizations import HUMIDITY, WIND, weather_conditions


class CityWeather:
    """
    A class representing weather data for a city.
    Initializes attributes based on the keys in the response dictionary.
    """

    def __init__(self, response_dict: dict, lang: str = "en"):
        self.lang = lang
        location = response_dict.get("location", {})
        self.name = location.get("name", "Unknown")
        self.country = location.get("country", "Unknown")
        self.region = location.get("region", "Unknow")
        self.localtime = location.get(
            "localtime", datetime.now().strftime("%A, %d %B, %H:%M")
        )
        self.lat = str(location.get("lat", 0.0))
        self.lon = str(location.get("lon", 0.0))

        current = response_dict.get("current", {})
        self.is_day = current.get("is_day", 0)
        self._temp_c = current.get("temp_c", 0.0)
        self._wind_kph = current.get("wind_kph", 0.0)
        self._wind_dir = current.get("wind_dir", "Unknown")
        self.humidity = current.get("humidity", 0)
        self.condition_code = current.get("condition", {}).get("code", 1000)
        self.icon_src = "https:" + current.get("condition", {}).get(
            "icon", DEFAULT_ICON_SRC
        )
        # self.condition = self.get_condition_text()

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
    def icon_path(self):
        return get_weather_icon(self.get_icon_name(), self.icon_src)

    @property
    def condition_code(self):
        return self._condition_code

    @condition_code.setter
    def condition_code(self, value):
        if value == 1000 and not self.is_day:
            value += 1
        self._condition_code = value

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

    def get_formatted_name(self):
        return localize_city_name(self.name, self.lang).capitalize()

    def get_condition_text(self):
        return weather_conditions[self.condition_code][self.lang]

    def formatted_wind_kph(self):
        return WIND[self.lang].format(self._wind_kph)

    def formatted_humidity(self):
        return HUMIDITY[self.lang].format(self.humidity)

    def get_city_local_time(self):
        try:
            city_dt = datetime.strptime(self.localtime, "%H:%M")
            return city_dt.strftime("%H:%M")
        except ValueError:
            return datetime.now().strftime("%H:%M")

    def get_city_date(self):
        """
        Returns the formatted local date and time for the city.
        For English: e.g., "Saturday, 18 May, 00:40"
        For Russian: e.g., "Суббота, 18 Мая, 00:40"
        """
        try:
            city_dt = datetime.strptime(self.localtime, "%Y-%m-%d %H:%M")
        except ValueError:
            city_dt = datetime.now()
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

    def __repr__(self):
        return (
            f"CityWeather(name={self._name}, country={self._country}, "
            f"temp_c={self._temp_c}, wind_kph={self._wind_kph})"
        )

    def get_icon_name(self):
        return f"{self.condition_code}_{self.is_day}.png"

    def get_weather_data(self):
        return (
            self.name,
            self.get_city_date(),
            self.condition,
            self.temp_c,
            self.wind_kph,
            self._humidity,
        )

    def get_weather_data_small(self):
        return (
            self.name,
            self.get_city_date(),
            self.condition_code,
            self.temp_c,
        )

    def formated_data_for_favs(self):
        return {
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
        }
