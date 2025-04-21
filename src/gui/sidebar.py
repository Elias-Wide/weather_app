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
)


class SideBar(NavigationRail):
    """
    Class to create a sidebar menu using NavigationRail.
    It contains a list of destinations and a leading button.
    """

    def __init__(self):
        super().__init__(
            label_type=NavigationRailLabelType.ALL,
            width=100,
            min_extended_width=100,
            leading=FloatingActionButton(icon=Icons.SEARCH, text="Поиск"),
            group_alignment=-0.9,
            destinations=[
                NavigationRailDestination(
                    icon=Icons.FAVORITE_BORDER,
                    selected_icon=Icons.FAVORITE,
                    label="Избранное",
                ),
                NavigationRailDestination(
                    icon=Icon(Icons.BOOKMARK_BORDER),
                    selected_icon=Icon(Icons.BOOKMARK),
                    label="О проекте",
                ),
                NavigationRailDestination(
                    icon=Icons.SETTINGS_OUTLINED,
                    selected_icon=Icon(Icons.SETTINGS),
                    label_content=Text("Settings"),
                ),
            ],
        )
        self.on_change = lambda e: print(
            "Selected destination:", e.control.selected_index
        )
