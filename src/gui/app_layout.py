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
from src.constants import TOGGLE_BTN
from src.gui.widgets import SearchWidget, WeatherWidget
from src.gui.sidebar import SideBar
from src.gui.page_elements import CustomAppBar, CustomIconButton


class AppLayout(Row):
    def __init__(self, app, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page: Page = page
        self.city = ["Moscow", "Saint Petersburg"]
        self.sidebar = SideBar()
        self.toggle_nav_rail_button = IconButton(
            key=TOGGLE_BTN,
            icon=Icons.ARROW_CIRCLE_LEFT,
            icon_color=Colors.BLUE_GREY_400,
            selected=False,
            selected_icon=Icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
        )

        self._active_view: Control = WeatherWidget()
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

    def toggle_nav_rail(self, e):
        print("Toggle nav rail")
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = (
            not self.toggle_nav_rail_button.selected
        )
        self.page.update()
