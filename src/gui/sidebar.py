from flet import (
    Column,
    Icon,
    Icons,
    FloatingActionButton,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    Container,
    IconButton,
    padding,
    margin,
)

from localizations import UI_LABELS
from src.constants import FAVORITE_VIEW, SEARCH_VIEW, WEATHER_VIEW


class SideBar(Container):
    """
    Class to create a sidebar menu using NavigationRail.
    It contains a list of destinations and a leading button.
    """

    def __init__(self, navigation_function, page):
        self.page = page
        self.navigation_function = navigation_function
        self.labels = ("WEATHER", "FAVORITES")
        self.top_nav_items = [
            NavigationRailDestination(
                data=WEATHER_VIEW,
                icon=Icons.CLOUD,
                selected_icon=Icons.CLOUD,
                label=UI_LABELS["WEATHER"][self.page.lang],
            ),
            NavigationRailDestination(
                data=FAVORITE_VIEW,
                icon=Icons.BOOKMARK_BORDER,
                selected_icon=Icon(Icons.BOOKMARK),
                label=UI_LABELS["FAVORITES"][self.page.lang],
            ),
        ]
        self.leading_button = FloatingActionButton(
            data=SEARCH_VIEW,
            width=170,
            icon=Icons.SEARCH,
            text=UI_LABELS["CITY_SEARCH"][self.page.lang],
            on_click=self.change_page_view,
        )
        self.toggle_nav_rail_button = IconButton(Icons.ARROW_BACK)
        self.top_nav_rail = NavigationRail(
            leading=self.leading_button,
            group_alignment=-0.9,
            selected_index=None,
            label_type=NavigationRailLabelType.ALL,
            on_change=self.change_page_view,
            destinations=self.top_nav_items,
            expand=True,
        )
        super().__init__(
            content=Column(
                [self.top_nav_rail],
                width=250,
                expand=True,
            ),
            padding=padding.all(15),
            margin=margin.all(0),
            width=250,
        )

    def change_page_view(self, e):
        """
        Function to change the page view.
        It is called when the user clicks on a destination.
        """
        if e.control.data == SEARCH_VIEW:
            self.top_nav_rail.selected_index = None
            self.navigation_function(SEARCH_VIEW)
        if not e.control.data:
            if e.control.selected_index == 0:
                self.navigation_function(WEATHER_VIEW)
            elif e.control.selected_index == 1:
                self.navigation_function(FAVORITE_VIEW)

    def change_lang(self):
        """
        Function to change the language of the sidebar.
        It is called when the user clicks on a destination.
        """
        for idx, item in enumerate(self.top_nav_items):
            item.label = UI_LABELS[self.labels[idx]][self.page.lang]
            item.update()
        self.leading_button.text = UI_LABELS["CITY_SEARCH"][self.page.lang]
        self.page.update()
