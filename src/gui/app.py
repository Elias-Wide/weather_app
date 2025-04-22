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
from constants import DWNLD, LANG_SWITCHER, THEME_SWITCHER, WEATHER_ICON

from src.config import APP_NAME, EN, RU
from src.gui.app_layout import AppLayout
from src.gui.sidebar import SideBar
from src.gui.page_elements import CustomAppBar, LoadingGif, WeatherIcon


class WeatherApp(AppLayout):
    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.user: str | None = None
        self.appbar = CustomAppBar(
            title=APP_NAME,
            lang=page.lang,
            change_theme_func=self.set_page_theme,
            change_language_func=self.set_page_language,
        )
        self.page.appbar = self.appbar

        self.page.update()
        super().__init__(
            self,
            self.page,
            tight=True,
            expand=True,
            vertical_alignment=CrossAxisAlignment.START,
        )

        # def initialize(self):
        #     self.page.views.append(
        #         View(
        #             "/",
        #             [self.appbar, self],
        #             padding=padding.all(0),
        #             bgcolor=Colors.BLUE_GREY_200,
        #         )
        #     )
        #     self.page.update()
        #     # create an initial board for demonstration if no boards
        #     if len(self.boards) == 0:
        #         self.create_new_board("My First Board")
        #     self.page.go("/")

        # def route_change(self, e):
        #     troute = TemplateRoute(self.page.route)
        #     if troute.match("/"):
        #         self.page.go("/boards")
        #     elif troute.match("/board/:id"):
        #         if int(troute.id) > len(self.store.get_boards()):
        #             self.page.go("/")
        #             return
        #         self.set_board_view(int(troute.id))
        #     elif troute.match("/boards"):
        #         self.set_all_boards_view()
        #     elif troute.match("/members"):
        #         self.set_members_view()
        #     self.page.update()

    def set_page_theme(self, e) -> None:
        """
        Function to set the theme of the page.
        """
        theme_switcher = self.get_appbar_action_by_key((THEME_SWITCHER,))
        if self.page.theme_mode == ThemeMode.DARK:
            self.page.theme_mode = ThemeMode.LIGHT
            theme_switcher.icon = Icons.WB_SUNNY
            theme_switcher.icon_color = Colors.YELLOW
        elif self.page.theme_mode == ThemeMode.LIGHT:
            self.page.theme_mode = ThemeMode.DARK
            theme_switcher.icon = Icons.NIGHTLIGHT
            theme_switcher.icon_color = Colors.BLUE
        self.page.update()

    def set_page_language(self, e) -> None:
        """
        Function to set the language of the page.
        It is called when the user clicks the button.
        """
        lang_switcher = self.get_appbar_action_by_key(LANG_SWITCHER)
        if self.page.lang == RU:
            self.page.lang = EN
            lang_switcher.text = EN
            # self.page.controls[0].actions[0].text = "EN"
        else:
            self.page.lang = RU
            lang_switcher.text = RU
        self.page.update()

    def add_download_gif(self) -> None:
        """
        Function to add a loading GIF to the page.
        It is called when the user submits the search input.
        """
        for control in self.page.controls:
            if isinstance(control, CustomAppBar):
                continue
            if control.key in (WEATHER_ICON, DWNLD):
                self.page.remove(control)
        self.page.add(LoadingGif(DWNLD))
        self.page.update()

    def get_appbar_action_by_key(self, control_keys: tuple[str]) -> None:
        """
        Function to get the action of a control based on its key."""
        for action in self.page.appbar.actions:
            if action.key in control_keys:
                return action
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

    def set_weather_icon(self) -> None:
        """
        Function to set the weather icon based on the current theme mode.
        It is called when the user clicks the button.
        """
        for control in self.page.controls:
            if isinstance(control, CustomAppBar):
                continue
            if control.key and control.key in (WEATHER_ICON, DWNLD):
                self.page.remove(control)
        self.page.add(WeatherIcon(name="dust"))
        self.page.update()
        self.page.update()
