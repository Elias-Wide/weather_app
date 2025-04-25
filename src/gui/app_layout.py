from flet import (
    ButtonStyle,
    Column,
    Colors,
    Control,
    Container,
    ControlState,
    IconButton,
    Icons,
    padding,
    Row,
    Page,
    Text,
    TextButton,
    TextThemeStyle,
    TextField,
    RoundedRectangleBorder,
    VerticalDivider,
    border,
    CrossAxisAlignment,
    alignment,
)

from src.config import APP_NAME
from src.constants import FAVORITE_VIEW, SEARCH_VIEW, TOGGLE_BTN, WEATHER_VIEW
from src.geo_ip import get_location
from src.gui.widgets import FavoriteWidget, SearchWidget, WeatherWidget
from src.gui.sidebar import SideBar
from src.gui.page_elements import CustomAppBar, CustomIconButton


class AppLayout(Row):
    def __init__(self, app, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page: Page = page
        self.city = "moscow"
        self.sidebar = SideBar(navigation_function=self.change_view)
        self.toggle_nav_rail_button = IconButton(
            key=TOGGLE_BTN,
            icon=Icons.ARROW_CIRCLE_LEFT,
            icon_color=Colors.BLUE_GREY_400,
            selected=False,
            selected_icon=Icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
        )
        self.city = "moscow"
        # self.city = get_location()
        self._active_view: Control = SearchWidget(self.city)
        self.controls = [
            self.sidebar,
            self.toggle_nav_rail_button,
            self.active_view,
        ]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.page.update()

    def change_view(self, view_type: str, *args, **kwargs):
        """Change the view of the app layout."""
        if view_type == SEARCH_VIEW:
            self.active_view = SearchWidget(*args, **kwargs)
        elif view_type == WEATHER_VIEW:
            self.active_view = WeatherWidget(self.city, *args, **kwargs)
        elif view_type == FAVORITE_VIEW:
            self.active_view = FavoriteWidget(*args, **kwargs)

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = (
            not self.toggle_nav_rail_button.selected
        )
        self.page.update()
