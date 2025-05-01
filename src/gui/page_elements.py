import datetime
from flet import (
    alignment,
    AppBar,
    Card,
    Colors,
    Column,
    ElevatedButton,
    Image,
    ImageFit,
    Icons,
    IconButton,
    Page,
    Row,
    Text,
    TextButton,
    TextField,
    TextThemeStyle,
    Container,
)

from database.dao import FavoritesDAO
from src.cityweather import CityWeather
from src.config import settings
from src.constants import (
    CHOOSE_CITY,
    CITY_NAME_ERROR,
    DEFAULT_ICON_SRC,
    GIF_PATH,
    LANG_SWITCHER,
    SEACRH_FIELD,
    THEME_SWITCHER,
    WEATHER_ICON,
    WEATHER_VIEW,
)
from src.parse_api import get_city_weather


class CustomAppBar(AppBar):
    """
    A custom AppBar with language and theme switcher buttons.
    """

    def __init__(
        self,
        title: str,
        lang: str,
        change_theme_func,
        change_language_func,
        *args,
        **kwargs,
    ):
        """
        Initializes the CustomAppBar.

        Args:
            title (str): The title of the AppBar.
            lang (str): The current language.
            change_theme_func (callable): Function to change the theme.
            change_language_func (callable): Function to change the language.
        """
        super().__init__(
            title=Text(title),
            bgcolor=Colors.SURFACE,
            actions=[
                ElevatedButton(
                    key=LANG_SWITCHER,
                    text=settings.default_lang,
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
    """
    A custom IconButton with a default on_click behavior.
    """

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
        """
        Initializes the CustomIconButton.

        Args:
            key (str): The key for the button.
            icon (str): The icon to display.
            tooltip (str, optional): Tooltip text for the button.
            on_click_func (callable, optional): Function to execute on click.
            icon_color (str, optional): Color of the icon.
        """
        if not on_click_func:
            on_click_func = self.default_on_click
        super().__init__()
        self.key = key
        self.icon = icon
        self.tooltip = tooltip
        self.on_click = on_click_func

    def default_on_click(self, e):
        """
        Default on_click function for the CustomIconButton.
        It can be overridden by the user.

        Args:
            e: The event object.
        """
        print(f"Button {self.key} clicked!")


class LoadingGif(Image):
    """
    A class representing a loading GIF.
    """

    def __init__(
        self,
        name: str,
        width: int = 200,
        height: int = 200,
        fit: str = ImageFit.CONTAIN,
        opacity: float = 1.0,
        animate_opacity: int = 5000,
    ):
        """
        Initializes the LoadingGif.

        Args:
            name (str): The key for the GIF.
            width (int, optional): Width of the GIF. Defaults to 200.
            height (int, optional): Height of the GIF. Defaults to 200.
            fit (str, optional): How the image should fit. Defaults to ImageFit.CONTAIN.
            opacity (float, optional): Opacity of the GIF. Defaults to 1.0.
            animate_opacity (int, optional): Animation duration for opacity. Defaults to 5000.
        """
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
    """
    A custom search field for entering city names.
    """

    def __init__(self, page_view, *args, **kwargs):
        """
        Initializes the SearchField.

        Args:
            page_view: The parent page view.
        """
        super().__init__(
            key=SEACRH_FIELD,
            label=CHOOSE_CITY,
            autofocus=True,
            width=300,
            expand=False,
            border_color=Colors.BLUE,
            on_submit=self.search_city,
            on_change=self.typing_mode,
            on_blur=self.stop_typing,
        )
        self.page_view = page_view

    def typing_mode(self, e):
        """
        Changes the border color to yellow while typing.

        Args:
            e: The event object.
        """
        self.border_color = "yellow"
        self.label = CHOOSE_CITY
        self.page.update()

    def stop_typing(self, e):
        """
        Resets the border color to blue when typing stops.

        Args:
            e: The event object.
        """
        self.border_color = Colors.BLUE
        self.page.update()

    def search_city(self, e):
        """
        Searches for the city weather when the user submits the input.

        Args:
            e: The event object.
        """
        city_name = self.value.strip()
        if not city_name:
            return
        weather = get_city_weather(city_name)
        if not weather:
            self.border_color = "red"
            self.label = CITY_NAME_ERROR
            self.page.update()
            return
        self.page_view.last_weather_request = CityWeather(weather)
        e.control.value = ""
        self.page_view.change_view(WEATHER_VIEW)


class WeatherIcon(Image):
    """
    A class representing a weather icon.
    """

    def __init__(
        self,
        name: str,
        fit: str = ImageFit.CONTAIN,
        width: int = 50,
        height: int = 50,
    ):
        """
        Initializes the WeatherIcon.

        Args:
            name (str): The key for the icon.
            fit (str, optional): How the image should fit. Defaults to ImageFit.CONTAIN.
            width (int, optional): Width of the icon. Defaults to 50.
            height (int, optional): Height of the icon. Defaults to 50.
        """
        super().__init__(
            key=WEATHER_ICON,
            src=DEFAULT_ICON_SRC,
            width=width,
            height=height,
            fit=fit,
        )


class CityCard(Card):
    """
    A class representing a city card with weather information and city name.
    """

    def __init__(self, city: CityWeather, **kwargs):
        """
        Initializes the CityCard.

        Args:
            city_name (str): The name of the city.
            weather_key (str): The weather key for the city.
            temp (str): The temperature in the city.
        """
        self.city = city
        content = Container(
            Column(
                controls=[
                    Row(
                        controls=[
                            Container(
                                Column(
                                    [WeatherIcon("", width=150)],
                                    expand=True,
                                    width=180,
                                    height=150,
                                    alignment=alignment.center,
                                ),
                                width=180,
                                expand=True,
                                bgcolor="green",
                            ),
                            Column(
                                [
                                    Text(
                                        city.formatted_temp_c(),
                                        color=Colors.GREY,
                                        expand=True,
                                        size=20,
                                    ),
                                ],
                                expand=True,
                            ),
                        ],
                        alignment=alignment.center,
                        expand=True,
                        height=140,
                    ),
                    Row(
                        [
                            TextButton(
                                city.name, on_click=lambda e: print(e.control)
                            ),
                            Text(
                                str(datetime.datetime.now()).split()[0],
                                color=Colors.BLUE,
                                weight="bold",
                            ),
                        ],
                        alignment=alignment.bottom_left,
                    ),
                ]
            ),
            width=250,
            height=140,
            padding=10,
            alignment=alignment.center,
        )
        super().__init__(content=content, **kwargs)


class FavoritesButton(IconButton):
    def __init__(self, city: CityWeather, *args, **kwargs):
        self.city = city
        city_in_favs = FavoritesDAO.get_fav_city(
            **city.formated_data_for_favs()
        )
        if city_in_favs:
            icon = Icons.FAVORITE_OUTLINED
            on_click_func = self.delete_from_favs
        else:
            icon = Icons.FAVORITE_BORDER
            on_click_func = self.add_to_favs
        super().__init__(icon=icon, on_click=on_click_func, *args, **kwargs)

    def delete_from_favs(self, e):
        if FavoritesDAO.delete_object(**self.city.formated_data_for_favs()):
            self.icon = Icons.FAVORITE_BORDER
            self.on_click = self.add_to_favs
            self.update()

    def add_to_favs(self, e):
        FavoritesDAO.create(self.city.formated_data_for_favs())
        self.icon = Icons.FAVORITE_OUTLINED
        self.on_click = self.delete_from_favs
        self.update()
