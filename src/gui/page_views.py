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
    Image,
    ImageFit,
    padding,
    Row,
    Stack,
    Text,
    TextAlign,
    TextField,
    TextThemeStyle,
    MainAxisAlignment,
    ImageRepeat,
    Icons,
    CrossAxisAlignment,
)

from src.constants import CITY_IMAGE_PATH, FAVORITE_VIEW
from src.database.dao import FavoritesDAO
from src.functions import get_city_date
from src.gui.page_elements import CityCard, SearchField
from src.parse_api import get_weather_page_data


class SearchView(Column):
    """
    This class represents the main view of the application.
    It contains a search bar.
    """

    def __init__(self, page_view, *args, **kwargs):
        super().__init__(
            expand=True, alignment=alignment.bottom_right, *args, **kwargs
        )
        self.page_view = page_view
        self.controls = [
            Container(
                SearchField(page_view=page_view),
                alignment=alignment.center,
                bgcolor=Colors.BLUE_GREY,
                expand=True,
                padding=padding.only(left=10, right=10, top=10),
            )
        ]


class WeatherView(Column):
    """
    This class represents the weather view of the application.
    It contains an image and a weather condition in the City.
    """

    def __init__(self, city_data: dict[str], page_view, **kwargs):
        self.page_view = page_view
        city_data = {
            "city": "moscow",
            "lat": 55.7522,
            "lon": 37.6156,
            "datetime": "2025-04-28 23:01",
            "temp": 7.1,
            "condition": 1009,
            "wind_kph": 13.3,
            "wind_dir": "WSW",
            "humidity": 45,
        }

        controls = [
            Container(
                Column(
                    [],
                    expand=True,
                    # width=500,
                    alignment=alignment.center,
                ),
                # bgcolor=Colors.GREEN,
                expand=True,
            )
        ]
        for data in get_weather_page_data(city_data):
            controls[-1].content.controls.append(
                Card(
                    Row(
                        [
                            Text(
                                data,
                                text_align=TextAlign.CENTER,
                                theme_style=TextThemeStyle.BODY_LARGE,
                                expand=True,
                            )
                        ],
                        expand=True,
                        alignment=CrossAxisAlignment.CENTER,
                    ),
                )
            )
        super().__init__(
            controls=[Card(Column(controls), margin=5)], expand=True, **kwargs
        )


class FavoritesView(Column):
    """
    This class represents the vieww with favorite cities.
    """

    def __init__(self, favorites, page_view, *args, **kwargs):
        super().__init__(
            expand=True, alignment=alignment.bottom_right, *args, **kwargs
        )
        self.page_view = page_view
        if city_card_data:
            self.set_city_cards(city_card_data)
        else:
            self.controls.append(
                Container(
                    Card(
                        Row(
                            [
                                Text(
                                    "Избранное",
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
                                )
                            ],
                        ),
                    ),
                    alignment=alignment.center,
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
        print(obj.content.api_id)
        ###NEED CREATE REQUEST IN DB
        for city in city_card_data:
            if obj.content.city_name in city.values():
                city_card_data.remove(city)
                break

        self.page.controls[0].change_view(FAVORITE_VIEW)

    def drag_leave(self, e: DragTargetEvent):
        bucket_icon = self.controls[-1].content.content
        bucket_icon.color = None
        bucket_icon.update()

    def set_city_cards(self, city_card_info: dict[str]):
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
                            content=CityCard(
                                city_name=city["city_name"],
                                weather_key=city["weather_key"],
                                temp=city["temp"],
                            ),
                        ),
                        # expand=True,
                    )
                )
                fav_counter += 1
                city_num += 1


city_card_data = [
    {"city_name": "Moscow", "weather_key": "dust", "temp": "20"},
    {"city_name": "New York", "weather_key": "dust", "temp": "25"},
    {"city_name": "London", "weather_key": "dust", "temp": "15"},
    # {"city_name": "Tokyo", "weather_key": "dust", "temp": "18"},
    # {"city_name": "Paris", "weather_key": "dust", "temp": "12"},
    # {"city_name": "Sydney", "weather_key": "dust", "temp": "22"},
    # {"city_name": "Berlin", "weather_key": "dust", "temp": "16"},
    # {"city_name": "Dubai", "weather_key": "dust", "temp": "30"},
    # {"city_name": "Rome", "weather_key": "dust", "temp": "19"},
]
