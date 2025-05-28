from typing import Optional
from cachetools import TTLCache
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

from cityweather import CityWeather
from database.dao import FavoritesDAO, favorites_cache
from config import settings
from constants import (
    LANG_SWITCHER,
    SEACRH_FIELD,
    THEME_SWITCHER,
    WEATHER_ICON,
    WEATHER_VIEW,
)
from localizations import TITLE, get_city_name_en, UI_LABELS
from parse_api import get_city_weather, get_weather_icon

city_card_large_cache = TTLCache(maxsize=100, ttl=600)
city_card_cache = TTLCache(maxsize=100, ttl=600)


class CustomAppBar(AppBar):
    """
    A custom AppBar with language and theme switcher buttons.
    """

    def __init__(
        self,
        title: str,
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
                    text=settings.default_lang.upper(),
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

    def change_lang(self):
        self.title.value = TITLE[self.page.lang]
        self.update()


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
                label=UI_LABELS["CHOOSE_CITY"][page_view.page.lang],
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
        self.content.label = UI_LABELS["CHOOSE_CITY"][self.page_view.page.lang]
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
            self.content.label = UI_LABELS["CITY_NAME_ERROR"][
                self.page_view.page.lang
            ]
            self.page.update()
            return
        self.page_view.last_weather_request = CityWeather(
            weather, lang=self.page_view.page.lang
        )
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

    def __new__(cls, city: CityWeather, page_view, **kwargs):
        cache_key = (
            city.name,
            page_view.page.lang,
        )
        if cache_key in city_card_cache:
            return city_card_cache[cache_key]
        instance = super().__new__(cls)
        city_card_cache[cache_key] = instance
        return instance

    def __init__(self, city: CityWeather, page_view, **kwargs):
        """
        Initializes the CityCard.

        Args:
            city (CityWeather): The CityWeather object containing weather data for the city.
            page_view: The parent page view.
        """
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True
        self.city = city
        self.page_view = page_view
        content = Column(
            controls=[
                Row(
                    controls=[
                        Column(
                            [WeatherIcon(city.icon_path, width=140)],
                            expand=True,
                            width=170,
                            height=150,
                            alignment=alignment.center,
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
                                    city.get_formatted_name(),
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
            ],
            width=250,
            height=140,
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

    def __new__(cls, city: CityWeather, page_view, **kwargs):
        cache_key = (
            city.name,
            page_view.page.lang,
        )
        if cache_key in city_card_large_cache:
            return city_card_large_cache[cache_key]
        instance = super().__new__(cls)
        city_card_large_cache[cache_key] = instance
        return instance

    def __init__(self, city: CityWeather, page_view, **kwargs):
        """
        Initializes the CityCardLarge.

        Args:
            city (CityWeather): The CityWeather object containing weather data for the city.
            page_view: The parent page view.
        """
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

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
                                    city.get_condition_text(),
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
        self.content = Column(
            [
                TextRow(
                    city.get_formatted_name(),
                    style=TextThemeStyle.DISPLAY_MEDIUM,
                ),
                TextRow(
                    city.get_city_date(), style=TextThemeStyle.BODY_MEDIUM
                ),
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
        """
        Removes the city from the favorites list.

        Args:
            e: The event object.
        """
        if FavoritesDAO.delete_object(**self.city.formated_data_for_favs()):
            self.icon = Icons.FAVORITE_BORDER
            self.on_click = self.add_to_favs
            self.update()
            favorites_cache.clear()

    def add_to_favs(self, e):
        """
        Adds the city to the favorites list.

        Args:
            e: The event object.
        """
        FavoritesDAO.create(self.city.formated_data_for_favs())
        self.icon = Icons.FAVORITE_OUTLINED
        self.on_click = self.delete_from_favs
        favorites_cache.clear()
        self.update()


class TextRow(Row):
    """
    A row containing a single centered text element.
    """

    def __init__(
        self, text: str, style: Optional[TextThemeStyle], *args, **kwargs
    ):
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

    def get_appbar_action_by_key(self, control_key: str) -> None:
        for action in self.page.appbar.actions:
            if action.key == control_key:
                return action
