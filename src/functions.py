from enum import Enum
from typing import Any
from flet import (
    Colors,
    Column,
    ElevatedButton,
    IconButton,
    Icons,
    Image,
    Page,
    ThemeMode,
)
import requests

from constants import DWNLD, GIF_PATH, WEATHER_ICON, WEATHER_ICON_PATH
from config import API_KEY, API_URL
from src.widget import CustomAppBar, LoadingGif, WeatherIcon


def set_page_theme_icon(page: Page) -> None:
    """
    Function to get the theme icon based on the current theme mode.
    """
    if page.theme_mode == ThemeMode.DARK:
        page.theme_mode = ThemeMode.LIGHT
        action = get_controls_action(page.controls, CustomAppBar, IconButton)
        action.icon = Icons.WB_SUNNY
        action.icon_color = Colors.YELLOW
    elif page.theme_mode == ThemeMode.LIGHT:
        page.theme_mode = ThemeMode.DARK
        action = get_controls_action(page.controls, CustomAppBar, IconButton)
        action.icon = Icons.NIGHTLIGHT
        action.icon_color = Colors.BLUE
        # if isinstance(control, CustomAppBar):
        #     for action in control.actions:
        #         if isinstance(action, IconButton):
        #             action.icon = Icons.NIGHTLIGHT
        # action.icon_color = Colors.BLUE
        # control.actions[0].icon = Icons.NIGHTLIGHT
        # control.actions[0].icon_color = Colors.BLUE
        # page.controls[0].actions[1].icon = Icons.NIGHTLIGHT
        # page.controls[0].actions[1].icon_color = Colors.BLUE
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
    print(page.controls)
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


def find_page_control(page: Page, control_name: str) -> None:
    """
    Function to find a control in the page by its name.
    It is called when the user submits the search input.
    """
    for control in page.controls:
        if isinstance(control, CustomAppBar):
            continue
        if control.key == control_name:
            return control
    return None


def get_controls_action(controls, control_type, action_type):
    """
    Function to get the action of a control based on its type.
    """
    for control in controls:
        if isinstance(control, control_type):
            for action in control.actions:
                if isinstance(action, action_type):
                    return action
