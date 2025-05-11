# WeatherApp

WeatherApp is an application designed to display current weather information for selected cities. It provides a user-friendly interface to view weather details such as temperature, humidity, wind speed, and more.

---

## Features

- **Current Weather Display**: View temperature, humidity, wind speed, weather conditions, and more.
- **Favorites Support**: Add cities to a favorites list for quick access.
- **Multilingual Support**: Supports multiple languages, including English (EN) and Russian (RU).
- **Theme Switching**: Toggle between light and dark themes.
- **Cross-Platform**: Works on Windows, macOS, Linux, Android, iOS, and web browsers.
- **Weather API Integration**: Fetch real-time weather data from Weather API.

---

## Project Structure

- **`src/`**: Main directory containing the application source code.
  - **`database/`**: Models and database management.
  - **`gui/`**: User interface components and pages.
  - **`assets/`**: Static files such as weather icons.
  - **`config/`**: Configuration files and application settings.
  - **`parse_api.py`**: Logic for interacting with the Weather API.
  - **`weather_conditions.py`**: Dictionary of weather conditions with translations.

- **`pyproject.toml`**: Dependency and project configuration file.
- **`README.md`**: Project documentation.
- **`.env`**: File for storing environment variables like API keys.

---

## Environment Variables

The application requires an `.env` file to be configured. Example content:

```plaintext
weather_api_token=your_weather_api_token_here
api_url=https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no&lang=eng
app_name=WeatherApp
app_version=0.1.0
ip_info_token=your_ip_info_token_here
default_lang=EN
db_name=app_db
```

---

## Dependencies

The project uses the following key dependencies:

- **flet**: For building the user interface.
- **sqlalchemy**: For database management.
- **pydantic-settings**: For managing application settings.
- **requests**: For interacting with the Weather API.
- **mtranslate**: For text translations.

The full list of dependencies can be found in the `pyproject.toml` file.
