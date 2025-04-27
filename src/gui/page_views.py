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
    TextField,
    TextThemeStyle,
    MainAxisAlignment,
    ImageRepeat,
    Icons,
    CrossAxisAlignment,
)

from src.constants import CITY_IMAGE_PATH, FAVORITE_VIEW
from src.gui.page_elements import CityCard, SearchField


class SearchWidget(Column):
    """
    This class represents the main view of the application.
    It contains a search bar.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            expand=True, alignment=alignment.bottom_right, *args, **kwargs
        )
        self.controls = [
            Container(
                SearchField(),
                alignment=alignment.center,
                bgcolor=Colors.BLUE_GREY,
                expand=True,
                padding=padding.only(left=10, right=10, top=10),
            )
        ]


class WeatherWidget(Column):
    """
    This class represents the weather view of the application.
    It contains an image and a weather condition in the City.
    """

    def __init__(self, city: str, **kwargs):
        print(city)
        print(CITY_IMAGE_PATH.format("moscow".lower()))
        super().__init__(**kwargs)
        self.controls = [
            Container(
                Row(
                    controls=[
                        Stack(
                            [
                                Image(
                                    src=CITY_IMAGE_PATH.format(city.lower()),
                                    # width=700,
                                    # height=700,
                                    fit=ImageFit.CONTAIN,
                                    expand=True,
                                    # expand_loose=True,
                                    # repeat=ImageRepeat.REPEAT,
                                    border_radius=border.all(30),
                                    # fit="cover",
                                ),
                                Text(
                                    "Image title",
                                    color="white",
                                    theme_style=TextThemeStyle.TITLE_LARGE,
                                    weight="bold",
                                    opacity=0.5,
                                    expand=True,
                                ),
                            ],
                            expand=True,
                        ),
                        Container(
                            Column(
                                [
                                    Text(
                                        city,
                                        theme_style=TextThemeStyle.TITLE_LARGE,
                                        color=Colors.WHITE,
                                        expand=True,
                                        width=250,
                                    ),
                                ],
                                expand=True,
                            ),
                            expand=True,
                            bgcolor=Colors.BLUE_GREY,
                        ),
                    ],
                    alignment=alignment.center,
                    expand=True,
                    tight=True,
                ),
                expand=True,
                bgcolor=Colors.GREEN,
            ),
        ]


class FavoriteWidget(Column):
    """
    This class represents the vieww with favorite cities.
    """

    def __init__(self, favorites: int = 6, *args, **kwargs):
        super().__init__(
            expand=True, alignment=alignment.bottom_right, *args, **kwargs
        )

        self.set_city_cards(city_card_data)
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
                    bgcolor="red",
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
    {"city_name": "Tokyo", "weather_key": "dust", "temp": "18"},
    {"city_name": "Paris", "weather_key": "dust", "temp": "12"},
    {"city_name": "Sydney", "weather_key": "dust", "temp": "22"},
    {"city_name": "Berlin", "weather_key": "dust", "temp": "16"},
    {"city_name": "Dubai", "weather_key": "dust", "temp": "30"},
    {"city_name": "Rome", "weather_key": "dust", "temp": "19"},
]
