from flet import (
    Colors,
    CrossAxisAlignment,
    Icons,
    Page,
    ThemeMode,
)
from constants import (
    DWNLD,
    EN,
    LANG_SWITCHER,
    RU,
    THEME_SWITCHER,
    WEATHER_ICON,
)

from src.config import settings
from src.gui.app_layout import AppLayout
from src.gui.sidebar import SideBar
from src.gui.page_elements import CustomAppBar, WeatherIcon


class WeatherApp(AppLayout):
    """
    A class representing the main Weather App layout.
    """

    def __init__(self, page: Page) -> None:
        """
        Initializes the WeatherApp.

        Args:
            page (Page): The main page object for the application.
        """
        self.page: Page = page
        self.user: str | None = None
        self.appbar = CustomAppBar(
            title=settings.app_name,
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
        else:
            self.page.lang = RU
            lang_switcher.text = RU
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
