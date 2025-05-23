# WeatherApp

WeatherApp is an application designed to display current weather information for selected cities. It provides a user-friendly interface to view weather details such as temperature, humidity, wind speed, and more.  
The application uses [weatherapi.com](https://weatherapi.com) as its source for real-time weather data.  
The project is built using the **Flet** framework, which enables the creation of cross-platform user interfaces.

---

## Features

- **Current Weather Display**: View temperature, humidity, wind speed, weather conditions, and more.
- **Favorites Support**: Add cities to a favorites list for quick access.
- **Multilingual Support**: Supports multiple languages, including English (EN) and Russian (RU).
- **Theme Switching**: Toggle between light and dark themes.
- **Cross-Platform**: Works on Windows, macOS, Linux, Android, iOS, and web browsers.
- **Weather API Integration**: Fetch real-time weather data from Weather API.
- **Weather Data Caching**: Weather data for each city is cached; API requests are made no more than once every 10 minutes per city.
- **Weather Icon Caching**: Weather icons are downloaded from the service as requests are made. Each icon is then saved locally to avoid repeated requests in the future.

---

## Project Structure

- **`src/`**: Main directory containing the application source code.
  - **`assets/`**: Static files such as weather icons and images.
  - **`config/`**: Configuration files and application settings.
  - **`constants.py`**: Common constants used throughout the app.
  - **`cityweather.py`**: Data model and logic for city weather representation.
  - **`database/`**: Database models and management logic.
  - **`gui/`**: User interface components, widgets, and page views.
    - **`app.py`**: Main application logic and layout.
    - **`page_elements.py`**: UI elements and widgets.
    - **`page_views.py`**: Page views and navigation.
    - **`sidebar.py`**: Sidebar navigation logic.
  - **`localizations.py`**: Localization logic and dictionaries for UI and weather conditions.
  - **`parse_api.py`**: Logic for interacting with the Weather API and caching.
- **`pyproject.toml`**: Dependency and project configuration file.
- **`README.md`**: Project documentation.
- **`.env` / `main.env`**: File for storing environment variables like API keys.
- **`venv/`**: Virtual environment directory (should be in `.gitignore`).

---

## Environment Variables

The application requires an `.env` file to be configured. Example content:

```plaintext
api_url=https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no&lang=eng
app_name=WeatherApp
app_version=0.1.0
default_lang=en
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
- **cachetools**: For caching API responses.

The full list of dependencies can be found in the `pyproject.toml` file.

---

## Running the Project

To run the project, follow these steps:

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - **Windows (Command Prompt)**:
     ```bash
     venv\Scripts\activate
     ```
   - **Windows (PowerShell)**:
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   flet run
   ```

### Optional: Run the project using `uv`

If you have `uv` installed, you can also run the project using the following commands:

1. **Create a virtual environment using `uv`**:
   ```bash
   uv venv .venv
   ```

2. **Activate the virtual environment**:
   - **Windows (Command Prompt)**:
     ```bash
     sorce .venv\Scripts\activate
     ```

   - **Linux/macOS**:
     ```bash
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   flet run
   ```

---

## Weather API Keys

The available API keys for the Weather API are stored in the `weather_api.txt` file. The application reads the key from this file to interact with the Weather API. Ensure that the file contains a valid API key in the following format:

```plaintext
your_api_key_here
```
