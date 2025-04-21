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

from src.widgets import SearchField


class SearchView(Column):
    """
    This class represents the main view of the application.
    It contains a search bar.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controls = [SearchField()]


class WeatherView(Column):
    """
    This class represents the weather view of the application.
    It contains an image and a weather condition in the City.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controls = [
            Row(
                [
                    Stack(
                        Image(
                            src="storage/data/new york.png",
                            width=200,
                            height=200,
                            fit="contain",
                        ),
                        Text(
                            value="WEATHER VIEW",
                            theme_style=TextThemeStyle.HEADLINE_MEDIUM,
                        ),
                    ),
                ]
            ),
            Row(
                [
                    SearchField(),
                ]
            ),
        ]
