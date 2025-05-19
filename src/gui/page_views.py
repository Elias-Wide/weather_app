import time
from flet import (
    alignment,
    border,
    Card,
    Colors,
    Column,
    Container,
    Draggable,
    DragTarget,
    DragTargetEvent,
    IconButton,
    ProgressRing,
    Image,
    ImageFit,
    padding,
    Row,
    Stack,
    Text,
    TextAlign,
    TextButton,
    TextThemeStyle,
    MainAxisAlignment,
    ImageRepeat,
    Icons,
    CrossAxisAlignment,
)

from localizations import UI_LABELS
from parse_api import get_city_weather, get_weather_icon
from src.cityweather import CityWeather
from src.constants import (
    DOWNLOAD_VIEW,
    FAVORITE_VIEW,
    SEARCH_VIEW,
    WEATHER_VIEW,
)
from src.database.dao import favorites_cache
from src.database.dao import FavoritesDAO
from src.gui.page_elements import (
    CityCard,
    CityCardLarge,
    FavoritesButton,
    SearchField,
    WeatherIcon,
)


class SearchView(Column):
    """
    This class represents the main view of the application.
    It contains a search bar.
    """

    view_type = SEARCH_VIEW

    def __init__(self, page_view, *args, **kwargs):
        super().__init__(
            expand=True, alignment=alignment.bottom_right, *args, **kwargs
        )
        self.page_view = page_view
        self.controls = [
            Container(
                SearchField(page_view=page_view),
                alignment=alignment.center,
                expand=True,
                padding=padding.only(left=10, right=10, top=10),
            )
        ]


class WeatherView(Column):
    """
    This class represents the weather view of the application.
    It contains an image and a weather condition in the City.
    """

    view_type = WEATHER_VIEW

    def __init__(self, page_view, *args, **kwargs):
        """
        Initializes the WeatherView.

        Args:
            page_view: The parent page view instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            expand=True,
            alignment=CrossAxisAlignment.END,
            *args,
            **kwargs,
        )
        self.page_view = page_view
        city: CityWeather = page_view.last_weather_request
        self.controls = [
            Container(
                Card(
                    Row(
                        [
                            CityCardLarge(city, page_view),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    expand=True,
                    color=Colors.SURFACE,
                ),
                expand=True,
            ),
        ]

    def __repr__(self):
        """
        Returns a string representation of the WeatherView.
        """
        return f"{self.view_type} | {super().__str__()}"


class FavoritesView(Column):
    """
    This class represents the view with favorite cities.
    """

    view_type = FAVORITE_VIEW

    def __init__(self, page_view, *args, **kwargs):
        """
        Initializes the FavoritesView.

        Args:
            page_view: The parent page view instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            expand=True, alignment=alignment.bottom_right, *args, **kwargs
        )
        self.page_size = 6
        self.page_view = page_view
        self.page_num = 1
        favs_cities, self.total_favs = FavoritesDAO.get_favorites_by_page()
        self.list_cities = [
            CityWeather(get_city_weather(city.name), self.page_view.page.lang)
            for city in favs_cities
        ]

        if not self.list_cities:
            self.controls.append(
                Container(
                    Card(
                        Row(
                            [
                                Text(
                                    UI_LABELS["FAVORITES"][
                                        self.page_view.page.lang
                                    ],
                                    text_align=TextAlign.CENTER,
                                    expand=True,
                                    color=Colors.GREY,
                                ),
                            ],
                            alignment=CrossAxisAlignment.CENTER,
                            expand=True,
                        ),
                        expand=True,
                    ),
                    expand=True,
                ),
            )
        else:
            self.set_favorites_page_view()

    def set_favorites_page_view(self):
        """
        Updates the controls to display the current page of favorite cities,
        including pagination controls and drag target for deleting favorites.
        """
        self.controls = []
        has_prev = self.page_num > 1
        has_next = self.page_num * self.page_size < self.total_favs
        favs_cities, _ = FavoritesDAO.get_favorites_by_page(
            self.page_num, self.page_size
        )
        list_cities = [
            CityWeather(get_city_weather(city.name), self.page_view.page.lang)
            for city in favs_cities
        ]
        self.set_city_cards(list_cities)
        if has_prev:
            self.controls.append(
                Row(
                    controls=[
                        IconButton(
                            Icons.NAVIGATE_BEFORE, on_click=self.get_prev_page
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    expand=True,
                )
            )
        if has_next:
            self.controls.append(
                Row(
                    controls=[
                        IconButton(
                            Icons.NAVIGATE_NEXT, on_click=self.get_next_page
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    expand=True,
                )
            )
        self.controls.append(
            DragTarget(
                group="color",
                content=Container(
                    content=Card(
                        Row(
                            controls=[
                                IconButton(
                                    icon=Icons.DELETE,
                                    expand=True,
                                    height=70,
                                    icon_size=45,
                                )
                            ],
                            expand=True,
                        ),
                    ),
                    alignment=alignment.center,
                    height=70,
                ),
                on_will_accept=self.drag_will_accept,
                on_accept=self.drag_accept,
                on_leave=self.drag_leave,
            ),
        )

    def get_next_page(self, e):
        """
        Switches to the next page of favorite cities.

        Args:
            e: The event object.
        """
        self.page_num += 1
        self.set_favorites_page_view()
        self.update()

    def get_prev_page(self, e):
        """
        Switches to the previous page of favorite cities.

        Args:
            e: The event object.
        """
        self.page_num -= 1
        self.set_favorites_page_view()
        self.page.update()

    def drag_will_accept(self, e: DragTargetEvent):
        """
        Handles the event when a draggable item is hovered over the drag target.

        Args:
            e (DragTargetEvent): The drag event.
        """
        bucket_icon = self.controls[-1].content.content
        bucket_icon.color = "red"
        bucket_icon.update()

    def drag_accept(self, e: DragTargetEvent):
        """
        Handles the event when a draggable item is dropped onto the drag target.

        Args:
            e (DragTargetEvent): The drag event.
        """
        bucket_icon = self.controls[-1].content.content
        bucket_icon.color = None
        bucket_icon.update()
        src_id = e.src_id
        obj = self.page.get_control(src_id)
        city: CityWeather = obj.content.city
        FavoritesDAO.delete_object(**city.formated_data_for_favs())
        favorites_cache.clear()
        self.page.controls[0].change_view(FAVORITE_VIEW)

    def drag_leave(self, e: DragTargetEvent):
        """
        Handles the event when a draggable item leaves the drag target area.

        Args:
            e (DragTargetEvent): The drag event.
        """
        bucket_icon = self.controls[-1].content.content
        bucket_icon.color = None
        bucket_icon.update()

    def set_city_cards(self, city_card_info: list[CityWeather]):
        """
        Arranges city cards in rows for the current page of favorites.

        Args:
            city_card_info (list[CityWeather]): List of CityWeather objects for the page.
        """
        city_num = 0
        self.controls = []
        while city_num != len(city_card_info):
            fav_counter = 0
            self.controls.append(
                Container(
                    Row(expand=True, alignment=CrossAxisAlignment.CENTER),
                    expand=True,
                    padding=30,
                ),
            )
            while fav_counter != 3:
                if city_num == len(city_card_info):
                    break
                city = city_card_info[city_num]
                self.controls[-1].content.controls.append(
                    Container(
                        Draggable(
                            group="color",
                            content=CityCard(city, self.page_view),
                        ),
                    )
                )
                fav_counter += 1
                city_num += 1


class DownloadView(Row):
    """
    This class represents the download (loading) view of the application.
    It displays a progress ring while data is being loaded.
    """

    view_type = DOWNLOAD_VIEW

    def __init__(self, page_view, *args, **kwargs):
        """
        Initializes the DownloadView.

        Args:
            page_view: The parent page view instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            expand=True,
            alignment=CrossAxisAlignment.CENTER,
        )
        self.controls = [
            Column(
                [
                    Container(
                        ProgressRing(
                            width=100,
                            height=100,
                            expand=True,
                            animate_opacity=True,
                        ),
                        alignment=alignment.center,
                        expand=True,
                    )
                ],
                expand=True,
            )
        ]
        self.page_view = page_view
