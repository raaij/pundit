import dash_bootstrap_components as dbc
from dash import html

PUNDIT_LOGO = "https://www.linkpicture.com/q/banner_16.png"

navbar = dbc.Container(
    dbc.Navbar(
        children=[
            dbc.NavItem(
                "Website Design Optimizer v1",
            ),
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Results", href="/results")),
            dbc.Col(html.Img(src=PUNDIT_LOGO, height="75px")),
            dbc.Col(dbc.NavbarBrand("decision support system for website design optimization", className="ms-2")),
        ]
    ),
    fluid=True,
)
