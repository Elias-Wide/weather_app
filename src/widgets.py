from flet import (
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
from src.constants import CHOOSE_CITY, GIF_PATH, WEATHER_ICON_PATH
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
                    text=DEFAULT_LANG,
                    on_click=change_language_func,
                    icon=Icons.LANGUAGE,
                ),
                IconButton(
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

    def __init__(self, key: str, icon: str, tooltip: str, on_click_func):
        super().__init__(
            icon=icon,
            tooltip=tooltip,
            on_click=on_click_func,
            icon_color=Colors.BLUE,
        )


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
        width: int = 50,
        height: int = 50,
        fit: str = ImageFit.CONTAIN,
    ):
        super().__init__(
            key="weather_icon",
            src=WEATHER_ICON_PATH.format(name),
            width=width,
            height=height,
            fit=fit,
        )
