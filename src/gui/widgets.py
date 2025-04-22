import time
from flet import (
    alignment,
    Colors,
    Column,
    Container,
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
)

from src.constants import CITY_IMAGE_PATH
from src.gui.page_elements import SearchField


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

    def __init__(self, **kwargs):
        print(CITY_IMAGE_PATH.format("moscow"))
        super().__init__(**kwargs)
        self.controls = [
            Container(
                Row(
                    controls=[
                        Stack(
                            [
                                Image(
                                    src=CITY_IMAGE_PATH.format("moscow"),
                                    # width=700,
                                    # height=700,
                                    fit=ImageFit.CONTAIN,
                                    expand=True,
                                    expand_loose=True,
                                    repeat=ImageRepeat.REPEAT,
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
                        ),
                        Container(
                            Column(
                                [
                                    Text(
                                        "Weather in City",
                                        theme_style=TextThemeStyle.TITLE_LARGE,
                                        color=Colors.WHITE,
                                        expand=True,
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
                ),
                expand=True,
                bgcolor=Colors.GREEN,
            ),
        ]
