from enum import Enum
from flet import Colors, Column, Icons, Image, Page, ThemeMode
import requests

from constants import DWNLD, GIF_PATH, WEATHER_ICON, WEATHER_ICON_PATH
from config import API_KEY, API_URL
from src.widgets import CustomAppBar, LoadingGif, WeatherIcon


def set_page_theme_icon(page: Page) -> None:
    """
    Function to get the theme icon based on the current theme mode.
    """
    if page.theme_mode == ThemeMode.DARK:
        page.theme_mode = ThemeMode.LIGHT
        page.controls[0].actions[1].icon = Icons.WB_SUNNY
        page.controls[0].actions[1].icon_color = Colors.YELLOW
    elif page.theme_mode == ThemeMode.LIGHT:
        page.theme_mode = ThemeMode.DARK
        page.controls[0].actions[1].icon = Icons.NIGHTLIGHT
        page.controls[0].actions[1].icon_color = Colors.BLUE
    page.update()


def get_city_weather(city: str, lang: str) -> dict:
    """
    Function to find a city based on user input.
    It is called when the user submits the search input.
    """
    response = requests.get(
        API_URL.format(city_name=city, api_key=API_KEY, lang=lang)
    ).json()
    print(response, type(response))


def add_download_gif(page: Page) -> None:
    """
    Function to add a loading GIF to the page.
    It is called when the user submits the search input.
    """
    for control in page.controls:
        if isinstance(control, CustomAppBar):
            continue
        if control.key in (WEATHER_ICON, DWNLD):
            page.remove(control)
    page.add(LoadingGif(DWNLD))
    page.update()


def set_page_language(page: Page) -> None:
    """
    Function to set the language of the page.
    It is called when the user clicks the button.
    """
    if page.lang == "ru":
        page.lang = "en"
        page.controls[0].actions[0].text = "EN"
    else:
        page.lang = "ru"
        page.controls[0].actions[0].text = "RU"
    page.update()


def set_weather_icon(page: Page) -> None:
    """
    Function to set the weather icon based on the current theme mode.
    It is called when the user clicks the button.
    """
    for control in page.controls:
        if isinstance(control, CustomAppBar):
            continue
        if control.key in (WEATHER_ICON, DWNLD):
            page.remove(control)
    page.add(WeatherIcon(name="dust"))
    page.update()
    page.update()


#     # Add the loading GIF
# gif_image = Image(
#         src="assets/loading.gif",  # Path to your GIF file
#         width=200,
#         height=200,
#         fit=ImageFit.CONTAIN,
#     )
