from flet import (
    app,
    Page,
    ThemeMode,
)
from config import settings

from src.parse_api import (
    get_conditions_from_api,
    insert_weather_conditions_data,
)
from src.database.db import create_db_and_tables
from src.gui.app import WeatherApp


def main(page: Page):
    page.title = f"{settings.app_name} {settings.app_name}"
    page.adaptive = True
    page.theme_mode = ThemeMode.DARK
    page.lang = settings.default_lang
    app = WeatherApp(page)
    page.add(app)


app(main)
