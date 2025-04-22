from flet import (
    Column,
    Icon,
    Icons,
    FloatingActionButton,
    MainAxisAlignment,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    Row,
    Text,
    VerticalDivider,
    Colors,
    Container,
    border_radius,
    IconButton,
    alignment,
    padding,
    margin,
)


class SideBar(Container):
    """
    Class to create a sidebar menu using NavigationRail.
    It contains a list of destinations and a leading button.
    """

    def __init__(self):
        self.top_nav_items = [
            NavigationRailDestination(
                icon=Icons.FAVORITE_BORDER,
                selected_icon=Icons.FAVORITE,
                label="Избранное",
            ),
            NavigationRailDestination(
                icon=Icons.BOOKMARK_BORDER,
                selected_icon=Icon(Icons.BOOKMARK),
                label="О проекте",
            ),
        ]
        self.toggle_nav_rail_button = IconButton(Icons.ARROW_BACK)
        self.top_nav_rail = NavigationRail(
            leading=FloatingActionButton(
                width=170,
                icon=Icons.SEARCH,
                text="Поиск",
                on_click=self.change_page_view,
            ),
            group_alignment=-0.9,
            selected_index=None,
            label_type=NavigationRailLabelType.ALL,
            on_change=lambda e: print(
                "Selected destination:", e.control.selected_index
            ),
            destinations=self.top_nav_items,
            bgcolor=Colors.BLUE_GREY,
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
            bgcolor=Colors.BLUE_GREY,
        )
        self.on_change = lambda e: print(
            "Selected destination:", e.control.selected_index
        )

    def change_page_view(self, view):
        """
        Function to change the page view.
        It is called when the user clicks on a destination.
        """
        print(self.page.controls)
        # self.page.active_view = Column(
        #     [self.top_nav_rail, view],
        #     tight=True,
        # )
