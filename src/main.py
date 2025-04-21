import time
from flet import (
    app,
    AppBar,
    border,
    Colors,
    Column,
    Container,
    CrossAxisAlignment,
    ElevatedButton,
    Icons,
    IconButton,
    MainAxisAlignment,
    Page,
    Text,
    TextField,
    ThemeMode,
    VerticalDivider,
    Row,
)
from config import APP_NAME, APP_VERSION, DEFAULT_LANG, RU
from constants import CHOOSE_CITY, PNG, SEARCH_LBL

from functions import (
    add_download_gif,
    # get_city_weather,
    set_page_language,
    set_page_theme_icon,
    set_weather_icon,
)
from src.gui.app_layout import AppLayout
from src.gui.sidebar import SideBar
from src.widgets import CustomAppBar


# from functions import find_city


def main(page: Page):
    page.title = f"{APP_NAME} {APP_VERSION}"
    page.adaptive = True

    page.theme_mode = ThemeMode.DARK
    page.lang = DEFAULT_LANG

    def change_theme(e):
        """
        Function to change the theme of the page.
        It is called when the user clicks the button.
        """
        set_page_theme_icon(page)
        page.update()

    def change_language(e):
        """
        Function to change the language of the page.
        It is called when the user clicks the button.
        """
        set_page_language(page)

    page.add(
        CustomAppBar(
            title=APP_NAME,
            lang=page.lang,
            change_theme_func=change_theme,
            change_language_func=change_language,
        )
    )
    page.add(AppLayout(app=app, page=page))


app(main)
