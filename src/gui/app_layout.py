from flet import (
    ButtonStyle,
    Column,
    Colors,
    Control,
    Container,
    ControlState,
    IconButton,
    Icons,
    padding,
    Row,
    Page,
    Text,
    TextButton,
    TextThemeStyle,
    TextField,
    RoundedRectangleBorder,
    VerticalDivider,
    border,
    CrossAxisAlignment,
)

from src.config import APP_NAME
from src.gui.sidebar import SideBar
from src.widget import CustomAppBar


class AppLayout(Row):
    def __init__(self, app, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page: Page = page
        self.city = ["Moscow", "Saint Petersburg"]
        self.sidebar = Row(
            [
                SideBar(),
            ],
            width=100,
            height=100,
        )
        self.main_view = Column(
            [
                Row(
                    [
                        Container(
                            Text(
                                value="MAIN VIEW",
                                theme_style=TextThemeStyle.HEADLINE_MEDIUM,
                            ),
                            # expand=True,
                            # padding=padding.only(top=15),
                        ),
                    ]
                ),
                Row(
                    [
                        TextField(
                            hint_text="Search all boards",
                            autofocus=False,
                            content_padding=padding.only(left=10),
                            width=200,
                            height=40,
                            text_size=12,
                            border_color=Colors.BLACK26,
                            focused_border_color=Colors.BLUE_ACCENT,
                            suffix_icon=Icons.SEARCH,
                        )
                    ]
                ),
            ]
        )
        self.controls = [self.sidebar, self.main_view]
