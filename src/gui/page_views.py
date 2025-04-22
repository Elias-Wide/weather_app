from flet import View

from src.gui.sidebar import SideBar
from src.gui.widgets import SearchWidget


class SearchPageView(View):
    """
    This class represents the main view of the application.
    It contains a search bar.
    """

    def __init__(self, app, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.controls = [SideBar(), SearchWidget()]
