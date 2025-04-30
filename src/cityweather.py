class CityWeather:
    """
    A class representing weather data for a city.
    Initializes attributes based on the keys in the response dictionary.
    """

    def __init__(self, response_dict: dict):
        """
        Initializes the CityWeather object with data from the response dictionary.

        Args:
            response_dict (dict): A dictionary containing weather data for a city.
        """
        # Location attributes
        location = response_dict.get("location", {})
        self.name = location.get("name", "")
        self.country = location.get("country", "")
        self.lat = location.get("lat", 0.0)
        self.lon = location.get("lon", 0.0)
        self.tz_id = location.get("tz_id", "")
        self.localtime_epoch = location.get("localtime_epoch", 0)
        self.localtime = location.get("localtime", "")

        # Current weather attributes
        current = response_dict.get("current", {})
        self.last_updated_epoch = current.get("last_updated_epoch", 0)
        self.last_updated = current.get("last_updated", "")
        self.temp_c = current.get("temp_c", 0.0)
        self.temp_f = current.get("temp_f", 0.0)
        self.is_day = current.get("is_day", 0)
        self.condition = current.get("condition", {}).get("text", "")
        self.condition_icon = current.get("condition", {}).get("icon", "")
        self.condition_code = current.get("condition", {}).get("code", 0)
        self.wind_mph = current.get("wind_mph", 0.0)
        self.wind_kph = current.get("wind_kph", 0.0)
        self.wind_degree = current.get("wind_degree", 0)
        self.wind_dir = current.get("wind_dir", "")
        self.pressure_mb = current.get("pressure_mb", 0.0)
        self.pressure_in = current.get("pressure_in", 0.0)
        self.precip_mm = current.get("precip_mm", 0.0)
        self.precip_in = current.get("precip_in", 0.0)
        self.humidity = current.get("humidity", 0)
        self.cloud = current.get("cloud", 0)
        self.feelslike_c = current.get("feelslike_c", 0.0)
        self.feelslike_f = current.get("feelslike_f", 0.0)
        self.windchill_c = current.get("windchill_c", 0.0)
        self.windchill_f = current.get("windchill_f", 0.0)
        self.heatindex_c = current.get("heatindex_c", 0.0)
        self.heatindex_f = current.get("heatindex_f", 0.0)
        self.dewpoint_c = current.get("dewpoint_c", 0.0)
        self.dewpoint_f = current.get("dewpoint_f", 0.0)
        self.vis_km = current.get("vis_km", 0.0)
        self.vis_miles = current.get("vis_miles", 0.0)
        self.uv = current.get("uv", 0.0)
        self.gust_mph = current.get("gust_mph", 0.0)
        self.gust_kph = current.get("gust_kph", 0.0)
