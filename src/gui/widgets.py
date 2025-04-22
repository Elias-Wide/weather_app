from flet import (
    alignment,
    Colors,
    Column,
    Container,
    Image,
    padding,
    Row,
    Stack,
    Text,
    TextField,
    TextThemeStyle,
    MainAxisAlignment,
)

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
        super().__init__(**kwargs)
        self.controls = [
            Container(
                TextField(value="Moscow"),
                alignment=alignment.center,
                bgcolor=Colors.BLUE_GREY,
                expand=True,
                padding=padding.only(left=10, right=10, top=10),
            )
        ]
