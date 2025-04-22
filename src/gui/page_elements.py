from flet import (
    AlertDialog,
    AppBar,
    Image,
    ImageFit,
    Colors,
    Icons,
    ElevatedButton,
    IconButton,
    Page,
    Text,
    TextField,
)

from src.config import DEFAULT_LANG
from src.constants import (
    CHOOSE_CITY,
    GIF_PATH,
    LANG_SWITCHER,
    SEACRH_FIELD,
    THEME_SWITCHER,
    WEATHER_ICON,
    WEATHER_ICON_PATH,
)
from src.weather_api import get_city_weather


class CustomAppBar(AppBar):
    def __init__(
        self,
        title: str,
        lang: str,
        change_theme_func,
        change_language_func,
        *args,
        **kwargs,
    ):
        super().__init__(
            title=Text(title),
            bgcolor=Colors.SURFACE,
            actions=[
                ElevatedButton(
                    key=LANG_SWITCHER,
                    text=DEFAULT_LANG,
                    on_click=change_language_func,
                    icon=Icons.LANGUAGE,
                ),
                IconButton(
                    key=THEME_SWITCHER,
                    icon=Icons.NIGHTLIGHT,
                    tooltip="Change theme",
                    on_click=change_theme_func,
                    icon_color=Colors.BLUE,
                ),
            ],
            *args,
            **kwargs,
        )


class CustomIconButton(IconButton):

    def __init__(
        self,
        key: str,
        icon: str,
        tooltip: str = None,
        on_click_func=None,
        icon_color=Colors.BLUE,
        *args,
        **kwargs,
    ):
        if not on_click:
            on_click = self.default_on_click
        super().__init__()
        self.key = key
        self.icon = icon
        self.tooltip = tooltip
        self.on_click = on_click

    def default_on_click(self, e):
        """
        Default on_click function for the CustomIconButton.
        It can be overridden by the user.
        """
        print(f"Button {self.key} clicked!")


class LoadingGif(Image):
    def __init__(
        self,
        name: str,
        width: int = 200,
        height: int = 200,
        fit: str = ImageFit.CONTAIN,
        opacity: float = 1.0,
        animate_opacity: int = 5000,
    ):
        super().__init__(
            key=name,
            src=GIF_PATH.format("download"),
            width=width,
            height=height,
            fit=fit,
            opacity=opacity,
            animate_opacity=animate_opacity,
        )


class SearchField(TextField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            key=SEACRH_FIELD,
            label=CHOOSE_CITY,
            autofocus=True,
            width=300,
            expand=False,
            # adaptive=True,
            border_color=Colors.BLUE,
            on_submit=self.search_city,
        )

    def search_city(self, e):
        city_name = self.value.strip()
        print(f"City name: {city_name}")
        if not city_name:
            return
        print(f"{city_name}. Узнаю погоду...")
        # time.sleep(2)
        weather = get_city_weather(city_name, self.page.lang)
        e.control.value = ""
        self.page.update()


class WeatherIcon(Image):
    def __init__(
        self,
        name: str,
        fit: str = ImageFit.CONTAIN,
        width: int = 50,
        height: int = 50,
        # fit: str = ImageFCONTAIN,
    ):
        super().__init__(
            key=WEATHER_ICON,
            src=WEATHER_ICON_PATH.format(name),
            width=width,
            height=height,
            fit=fit,
        )


class DevAlert(AlertDialog):
    def __init__(self, title: str, on_dismiss: callable, *args, **kwargs):
        super().__init__(
            title=Text("Hello, you!"),
            on_dismiss=lambda e: print("Dialog dismissed!"),
            *args,
            **kwargs,
        )
