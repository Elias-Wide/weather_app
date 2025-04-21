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
            # NavigationRailDestination(
            #     icon=Icons.SETTINGS_OUTLINED,
            #     selected_icon=Icons.SETTINGS,
            #     label_content=Text("Settings"),
            # ),
        ]

        self.top_nav_rail = NavigationRail(
            leading=FloatingActionButton(
                width=170, icon=Icons.SEARCH, text="Поиск"
            ),
            group_alignment=-0.9,
            selected_index=None,
            label_type=NavigationRailLabelType.ALL,
            on_change=lambda e: print(
                "Selected destination:", e.control.selected_index
            ),
            destinations=self.top_nav_items,
            bgcolor=Colors.BLUE_GREY,
            extended=True,
            height=150,
        )
        super().__init__(
            content=Column(
                [self.top_nav_rail],
                tight=True,
            ),
            padding=padding.all(15),
            margin=margin.all(0),
            width=250,
            bgcolor=Colors.BLUE_GREY,
        )
        # super().__init__(
        #     content=Column(
        #         [
        #             Row(
        #                 [
        #                     Text("Workspace"),
        #                 ],
        #                 alignment=MainAxisAlignment.SPACE_BETWEEN,
        #             ),
        #             # divider
        #             Container(
        #                 bgcolor=Colors.BLACK26,
        #                 border_radius=border_radius.all(30),
        #                 height=1,
        #                 alignment=alignment.center_right,
        #                 width=220,
        #             ),
        #             self.top_nav_rail,
        #             # divider
        #             Container(
        #                 bgcolor=Colors.BLACK26,
        #                 border_radius=border_radius.all(30),
        #                 height=1,
        #                 alignment=alignment.center_right,
        #                 width=220,
        #             ),
        #             self.bottom_nav_rail,
        #         ],
        #         tight=True,
        #     ),
        # super().__init__(
        #     label_type=NavigationRailLabelType.ALL,
        #     width=100,
        #     height=200,
        #     min_extended_width=1,
        #     leading=FloatingActionButton(icon=Icons.SEARCH, text="Поиск"),
        #     group_alignment=-0.9,
        #     destinations=[
        #         NavigationRailDestination(
        #             icon=Icons.FAVORITE_BORDER,
        #             selected_icon=Icons.FAVORITE,
        #             label="Избранное",
        #         ),
        #         NavigationRailDestination(
        #             icon=Icon(Icons.BOOKMARK_BORDER),
        #             selected_icon=Icon(Icons.BOOKMARK),
        #             label="О проекте",
        #         ),
        #         NavigationRailDestination(
        #             icon=Icons.SETTINGS_OUTLINED,
        #             selected_icon=Icon(Icons.SETTINGS),
        #             label_content=Text("Settings"),
        #         ),
        #     ],
        # )

        self.on_change = lambda e: print(
            "Selected destination:", e.control.selected_index
        )
