import time
from flet import (
    AppBar,
    Page,
    app,
    Icons,
    Colors,
    ElevatedButton,
    IconButton,
    TextField,
    Column,
    MainAxisAlignment,
    CrossAxisAlignment,
    Text,
    ThemeMode,
)
from config import APP_NAME, APP_VERSION, DEFAULT_LANG, RU
from constants import CHOOSE_CITY, PNG, SEARCH_LBL

from functions import (
    add_download_gif,
    get_city_weather,
    set_page_language,
    set_page_theme_icon,
    set_weather_icon,
)
from src.widgets import CustomAppBar

# from functions import find_city


def main(page: Page):
    page.title = f"{APP_NAME} {APP_VERSION}"

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

    def change_weather_icon(e):
        """
        Function to change the weather icon based on the current theme mode.
        It is called when the user clicks the button.
        """
        set_weather_icon(page)

    def submit_text(e):
        """
        Function to find a city based on user input.
        It is called when the user submits the search input.
        """
        add_download_gif(page)
        city_name = e.control.value.strip()
        if not city_name:
            return
        print(f"{city_name}. Узнаю погоду...")
        print(f"Язык: {page.lang}")
        time.sleep(2)
        weather = get_city_weather(city_name, page.lang)
        change_weather_icon(e)
        e.control.value = ""
        page.update()

    page.add(
        CustomAppBar(
            title=APP_NAME,
            lang=RU,
            change_theme_func=change_theme,
            change_language_func=change_language,
        )
    )
    search_input = TextField(
        label=CHOOSE_CITY, autofocus=True, width=300, on_submit=submit_text
    )
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.add(
        Column(
            [
                search_input,
            ],
            # alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
    )


app(target=main, assets_dir="assets")
