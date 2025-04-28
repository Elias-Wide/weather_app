from flet import (
    app,
    Page,
    ThemeMode,
)
from config import APP_NAME, APP_VERSION, DEFAULT_LANG

from src.database.db import create_db_and_tables
from src.gui.app import WeatherApp


def main(page: Page):
    page.title = f"{APP_NAME} {APP_VERSION}"
    page.adaptive = True
    page.theme_mode = ThemeMode.DARK
    page.lang = DEFAULT_LANG
    app = WeatherApp(page)
    page.add(app)
    create_db_and_tables()


app(main)
