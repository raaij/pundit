import dash_bootstrap_components as dbc

navbar = dbc.Container(
    dbc.Navbar(
        children=[
            dbc.NavItem(
                "Website Design Optimizer v1",
            ),
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Results", href="/results")),
        ]
    ),
    fluid=True,
)
