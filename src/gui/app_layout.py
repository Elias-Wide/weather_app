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
from src.gui.widgets import SearchWidget
from src.gui.sidebar import SideBar
from src.gui.page_elements import CustomAppBar


class AppLayout(Row):
    def __init__(self, app, page: Page, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.app = app
        self.page: Page = page
        self.city = ["Moscow", "Saint Petersburg"]
        self.sidebar = Column(
            [
                SideBar(),
            ],
            tight=True,
            alignment=alignment.center,
        )
        self._active_view: Control = SearchWidget()
        self.controls = [self.sidebar, self.active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.page.update()
