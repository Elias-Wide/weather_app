from flet import Page

from constants import DWNLD, WEATHER_ICON
from src.config import APP_NAME
from src.gui.page_elements import CustomAppBar, LoadingGif


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
