from typing import Optional
from flet import (
    alignment,
    AppBar,
    Card,
    Colors,
    Column,
    CrossAxisAlignment,
    ElevatedButton,
    Image,
    ImageFit,
    Icons,
    IconButton,
    MainAxisAlignment,
    Row,
    Text,
    TextButton,
    TextField,
    TextAlign,
    TextThemeStyle,
    Container,
    ProgressRing,
)

from database.dao import FavoritesDAO
from functions import get_city_name_en
from src.cityweather import CityWeather
from src.config import settings
from src.constants import (
    CHOOSE_CITY,
    CITY_NAME_ERROR,
    LANG_SWITCHER,
    SEACRH_FIELD,
    THEME_SWITCHER,
    WEATHER_ICON,
    WEATHER_VIEW,
)
from src.parse_api import get_city_weather, get_weather_icon


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


class SearchField(Container):
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
            content=TextField(
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
        )
        self.page_view = page_view

    def typing_mode(self, e):
        """
        Changes the border color to yellow while typing.

        Args:
            e: The event object.
        """
        self.content.border_color = "yellow"
        self.content.label = ""
        self.page.update()

    def stop_typing(self, e):
        """
        Resets the border color to blue when typing stops.

        Args:
            e: The event object.
        """
        self.content.border_color = Colors.BLUE
        self.content.label = CHOOSE_CITY
        self.page.update()

    def search_city(self, e):
        """
        Searches for the city weather when the user submits the input.

        Args:
            e: The event object.
        """
        previous_widget = self.content
        city_name = get_city_name_en(self.content.value.strip())
        self.content = ProgressRing(width=100, height=100, expand=True)
        self.page.update()
        if not city_name:
            self.content = previous_widget
            self.page.update()
            return
        weather = get_city_weather(city_name)
        if not weather:
            self.content = previous_widget
            self.content.border_color = Colors.RED
            self.content.label = CITY_NAME_ERROR
            self.page.update()
            return
        self.page_view.last_weather_request = CityWeather(weather)
        self.page_view.change_view(WEATHER_VIEW)


class WeatherIcon(Image):
    """
    A class representing a weather icon.
    """

    def __init__(
        self,
        icon_path: str,
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
            src=icon_path,
            width=width,
            height=height,
            fit=fit,
        )


class CityCard(Card):
    """
    A class representing a city card with weather information and city name.
    """

    def __init__(self, city: CityWeather, page_view, **kwargs):
        """
        Initializes the CityCard.

        Args:
            city (CityWeather): The CityWeather object containing weather data for the city.
            page_view: The parent page view.
        """
        self.city = city
        self.page_view = page_view
        content = Container(
            Column(
                controls=[
                    Row(
                        controls=[
                            Container(
                                Column(
                                    [WeatherIcon(city.icon_path, width=140)],
                                    expand=True,
                                    width=170,
                                    height=150,
                                    alignment=alignment.center,
                                ),
                                width=180,
                                expand=True,
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
                            Row(
                                [
                                    TextButton(
                                        city.name,
                                        on_click=self.go_to_weather_page,
                                    )
                                ],
                                alignment=MainAxisAlignment.START,
                            ),
                            Row(
                                [
                                    Text(
                                        city.get_city_local_time(),
                                        color=Colors.BLUE,
                                        weight="bold",
                                    )
                                ],
                                alignment=MainAxisAlignment.END,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                ]
            ),
            width=250,
            height=140,
            padding=10,
            alignment=alignment.center,
        )
        super().__init__(content=content, **kwargs)

    def go_to_weather_page(self, e):
        self.page_view.last_weather_request = self.city
        self.page_view.active_download_view()
        self.page_view.change_view(WEATHER_VIEW)


class CityCardLarge(Card):
    """
    A class representing a larger city card with detailed weather information.
    """

    def __init__(self, city: CityWeather, page_view, **kwargs):
        """
        Initializes the CityCardLarge.

        Args:
            city (CityWeather): The CityWeather object containing weather data for the city.
            page_view: The parent page view.
        """
        super().__init__(width=600, height=400, **kwargs)
        self.city = city
        self.page_view = page_view
        city_condition_block = Row(
            [
                Container(
                    Column(
                        [
                            Container(
                                Image(
                                    src=city.icon_path,
                                ),
                                width=70,
                                alignment=alignment.top_right,
                                expand=True,
                            ),
                            Container(
                                Text(
                                    city.condition,
                                    theme_style=TextThemeStyle.HEADLINE_SMALL,
                                    text_align=TextAlign.CENTER,
                                ),
                                alignment=alignment.center,
                            ),
                        ],
                        alignment=CrossAxisAlignment.CENTER,
                    ),
                    alignment=alignment.center,
                ),
                Container(
                    Column(
                        [
                            Container(
                                Text(
                                    city.formatted_temp_c(),
                                    theme_style=TextThemeStyle.DISPLAY_LARGE,
                                    text_align=TextAlign.CENTER,
                                    size=25,
                                ),
                                alignment=alignment.center,
                            )
                        ],
                        height=100,
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    alignment=alignment.center,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
        )
        self.content = Container(
            Column(
                [
                    TextRow(city.name, style=TextThemeStyle.DISPLAY_MEDIUM),
                    TextRow(city.get_city_date(), style=TextThemeStyle.BODY_MEDIUM),
                    city_condition_block,
                    TextRow(
                        city.formatted_wind_kph(),
                        style=TextThemeStyle.BODY_MEDIUM,
                    ),
                    TextRow(
                        city.formatted_humidity(),
                        style=TextThemeStyle.BODY_MEDIUM,
                    ),
                    Row(
                        [FavoritesButton(city=city)],
                        expand=True,
                        alignment=MainAxisAlignment.END,
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
            alignment=alignment.center,
        )


class FavoritesButton(IconButton):
    """
    A button for adding or removing a city from the favorites list.
    """

    def __init__(self, city: CityWeather, *args, **kwargs):
        """
        Initializes the FavoritesButton.

        Args:
            city (CityWeather): The CityWeather object representing the city.
        """
        self.city = city
        city_in_favs = FavoritesDAO.get_fav_city(**city.formated_data_for_favs())
        if city_in_favs:
            icon = Icons.FAVORITE_OUTLINED
            on_click_func = self.delete_from_favs
        else:
            icon = Icons.FAVORITE_BORDER
            on_click_func = self.add_to_favs
        super().__init__(icon=icon, on_click=on_click_func, *args, **kwargs)

    def delete_from_favs(self, e):
        """
        Removes the city from the favorites list.

        Args:
            e: The event object.
        """
        if FavoritesDAO.delete_object(**self.city.formated_data_for_favs()):
            self.icon = Icons.FAVORITE_BORDER
            self.on_click = self.add_to_favs
            self.update()

    def add_to_favs(self, e):
        """
        Adds the city to the favorites list.

        Args:
            e: The event object.
        """
        FavoritesDAO.create(self.city.formated_data_for_favs())
        self.icon = Icons.FAVORITE_OUTLINED
        self.on_click = self.delete_from_favs
        self.update()


class TextRow(Row):
    """
    A row containing a single centered text element.
    """

    def __init__(self, text: str, style: Optional[TextThemeStyle], *args, **kwargs):
        """
        Initializes the TextRow.

        Args:
            text (str): The text to display.
            style (Optional[TextThemeStyle]): The text style.
        """
        super().__init__(*args, **kwargs)
        self.controls = [
            Text(
                text,
                text_align=TextAlign.CENTER,
                theme_style=style,
            )
        ]
        self.alignment = MainAxisAlignment.CENTER
