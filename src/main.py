from flet import (
    app,
    Page,
    ThemeMode,
)
from config import settings
from db_init import init_database
from src.gui.app import WeatherApp


def main(page: Page):
    page.title = f"{settings.app_name} {settings.app_name}"
    page.adaptive = True
    page.theme_mode = ThemeMode.DARK
    page.lang = settings.default_lang
    app = WeatherApp(page)
    page.add(app)
    init_database()


app(main)
