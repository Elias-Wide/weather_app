import time
from flet import (
    app,
    AppBar,
    border,
    Colors,
    Column,
    Container,
    CrossAxisAlignment,
    ElevatedButton,
    Icons,
    IconButton,
    MainAxisAlignment,
    Page,
    Text,
    TextField,
    ThemeMode,
    VerticalDivider,
    Row,
)
from config import APP_NAME, APP_VERSION, DEFAULT_LANG, RU
from constants import CHOOSE_CITY, PNG, SEARCH_LBL

from functions import add_download_gif

from src.gui.app import WeatherApp
from src.gui.app_layout import AppLayout
from src.gui.sidebar import SideBar
from src.gui.page_elements import CustomAppBar


# def initialize(self):
#     self.page.views.append(
#         View(
#             "/",
#             [self.appbar, self],
#             padding=padding.all(0),
#             bgcolor=Colors.BLUE_GREY_200,
#         )
#     )
#     self.page.update()
#     # create an initial board for demonstration if no boards
#     if len(self.boards) == 0:
#         self.create_new_board("My First Board")
#     self.page.go("/")

# def route_change(self, e):
#     troute = TemplateRoute(self.page.route)
#     if troute.match("/"):
#         self.page.go("/boards")
#     elif troute.match("/board/:id"):
#         if int(troute.id) > len(self.store.get_boards()):
#             self.page.go("/")
#             return
#         self.set_board_view(int(troute.id))
#     elif troute.match("/boards"):
#         self.set_all_boards_view()
#     elif troute.match("/members"):
#         self.set_members_view()
#     self.page.update()


def main(page: Page):
    page.title = f"{APP_NAME} {APP_VERSION}"
    page.adaptive = True
    page.theme_mode = ThemeMode.DARK
    page.lang = DEFAULT_LANG
    app = WeatherApp(page)
    # page.add(
    #     CustomAppBar(
    #         title=APP_NAME,
    #         lang=page.lang,
    #         change_theme_func=change_theme,
    #         change_language_func=change_language,
    #     )
    # )
    page.add(app)


app(main)
