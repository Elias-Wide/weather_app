from enum import Enum
import flet as ft
import requests

from constants import GIF_PATH, WEATHER_ICON_PATH
from config import API_KEY, API_URL


def set_page_theme_icon(page: ft.Page) -> None:
    """
    Function to get the theme icon based on the current theme mode.
    """
    if page.theme_mode == ft.ThemeMode.DARK:
        page.theme_mode = ft.ThemeMode.LIGHT
        page.controls[0].actions[1].icon = ft.Icons.WB_SUNNY
        page.controls[0].actions[1].icon_color = ft.Colors.YELLOW
    elif page.theme_mode == ft.ThemeMode.LIGHT:
        page.theme_mode = ft.ThemeMode.DARK
        page.controls[0].actions[1].icon = ft.Icons.NIGHTLIGHT
        page.controls[0].actions[1].icon_color = ft.Colors.BLUE
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


def add_download_gif(page: ft.Page) -> None:
    """
    Function to add a loading GIF to the page.
    It is called when the user submits the search input.
    """
    # Remove any existing GIFs before adding a new one
    for control in page.controls:
        if isinstance(control, ft.Image) and (
            "assets/gifs/download.gif" in control.src
            or "src/assets/weather_icons/" in control.src
        ):
            page.remove(control)
    page.add(
        ft.Image(
            src=GIF_PATH.format("download"),  # Path to your GIF file
            width=50,
            height=500,
            fit=ft.ImageFit.CONTAIN,
        )
    )
    page.update()


def set_page_language(page: ft.Page) -> None:
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


def set_weather_icon(page: ft.Page) -> None:
    """
    Function to set the weather icon based on the current theme mode.
    It is called when the user clicks the button.
    """
    print(page.controls)
    for control in page.controls:
        if isinstance(control, ft.Image) and control.src == GIF_PATH.format(
            "download"
        ):
            page.remove(control)
    page.add(
        ft.Image(
            src=WEATHER_ICON_PATH.format("sunset"),
            width=50,
            height=50,
        )
    )
    page.update()
    page.update()


#     # Add the loading GIF
# gif_image = ft.Image(
#         src="assets/loading.gif",  # Path to your GIF file
#         width=200,
#         height=200,
#         fit=ft.ImageFit.CONTAIN,
#     )
