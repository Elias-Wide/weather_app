from flet import (
    Control,
    IconButton,
    Icons,
    Row,
    Page,
)

from cityweather import CityWeather
from config import settings
from constants import FAVORITE_VIEW, SEARCH_VIEW, TOGGLE_BTN, WEATHER_VIEW
from gui.page_views import (
    DownloadView,
    FavoritesView,
    SearchView,
    WeatherView,
)
from gui.sidebar import SideBar


class AppLayout(Row):
    """
    A base layout class for the Weather App.
    Manages the sidebar, navigation, and active views.
    """

    def __init__(self, app, page: Page, *args, **kwargs):
        """
        Initializes the AppLayout.

        Args:
            app: The main application instance.
            page (Page): The Flet Page object for the application.
        """
        super().__init__(*args, **kwargs)
        self.expand = True
        self.app = app
        self.page: Page = page
        self.sidebar = SideBar(
            navigation_function=self.change_view, page=self.page
        )
        self.toggle_nav_rail_button = IconButton(
            key=TOGGLE_BTN,
            icon=Icons.ARROW_CIRCLE_LEFT,
            selected=False,
            selected_icon=Icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
        )
        self.last_weather_request: CityWeather | None = None
        self._active_view: Control = SearchView(page_view=self)
        self.controls = [
            self.sidebar,
            self.toggle_nav_rail_button,
            self.active_view,
        ]

    @property
    def active_view(self):
        """
        Gets the currently active view.

        Returns:
            Control: The currently active view.
        """
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        """
        Sets the active view and updates the layout.

        Args:
            view (Control): The new view to set as active.
        """
        self._active_view = view
        self.controls[-1] = self._active_view
        self.page.update()

    def change_view(self, view_type: str, *args, **kwargs):
        """
        Changes the view of the app layout based on the view type.

        Args:
            view_type (str): The type of view to switch to.
            *args: Additional arguments for the view.
            **kwargs: Additional keyword arguments for the view.
        """
        self.active_download_view()
        if view_type == FAVORITE_VIEW:
            new_view = FavoritesView
        elif view_type == SEARCH_VIEW or not self.last_weather_request:
            new_view = SearchView
        elif view_type == WEATHER_VIEW:
            new_view = WeatherView
        self.active_view = new_view(page_view=self, *args, **kwargs)

    def active_download_view(self, *args, **kwargs):
        """
        Activates the download view.

        Args:
            *args: Additional arguments for the view.
            **kwargs: Additional keyword arguments for the view.
        """
        self.active_view = DownloadView(page_view=self, *args, **kwargs)

    def toggle_nav_rail(self, e):
        """
        Toggles the visibility of the navigation rail (sidebar).

        Args:
            e: The event object triggered by the toggle button.
        """
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = (
            not self.toggle_nav_rail_button.selected
        )
        self.page.update()

    def change_lang(self):
        """
        Changes the language of the app layout.
        """
        self.sidebar.change_lang()
        view_type = self.active_view.view_type
        self.active_download_view()
        self.change_view(
            view_type,
        )
        self.page.update()
