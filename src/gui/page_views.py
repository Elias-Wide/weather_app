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
        return f"{self.view_type} | {super().__str__()}"


class FavoritesView(Column):
    """
    This class represents the vieww with favorite cities.
    """

    view_type = FAVORITE_VIEW

    def __init__(self, page_view, *args, **kwargs):
        super().__init__(
            expand=True, alignment=alignment.bottom_right, *args, **kwargs
        )
        self.page_view = page_view
        list_cities = [
            CityWeather(get_city_weather(city.name), self.page_view.page.lang)
            for city in FavoritesDAO.get_multi()
        ]
        if not list_cities:
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
            self.set_city_cards(list_cities)
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

    def drag_will_accept(self, e: DragTargetEvent):
        bucket_icon = self.controls[-1].content.content
        bucket_icon.color = "red"
        bucket_icon.update()

    def drag_accept(self, e: DragTargetEvent):  # DragTargetEvent
        bucket_icon = self.controls[-1].content.content
        bucket_icon.color = None
        bucket_icon.update()
        src_id = e.src_id
        obj = self.page.get_control(src_id)
        city: CityWeather = obj.content.city
        FavoritesDAO.delete_object(**city.formated_data_for_favs())
        self.page.controls[0].change_view(FAVORITE_VIEW)

    def drag_leave(self, e: DragTargetEvent):
        bucket_icon = self.controls[-1].content.content
        bucket_icon.color = None
        bucket_icon.update()

    def set_city_cards(self, city_card_info: list[CityWeather]):
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
            while fav_counter != 4:
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
    view_type = DOWNLOAD_VIEW

    def __init__(self, page_view, *args, **kwargs):
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
