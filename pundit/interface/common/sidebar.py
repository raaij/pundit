import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from pundit.interface.app import app

import pundit

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "right": 0,
    "width": "4rem",
    "padding": "5rem 1rem 1rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.Img(
            src=app.get_asset_url('logo-black.png'),
            style={
                "width": "2rem",
                "padding": "0rem 0rem",
            }
            # className="display-4"
        ),
        dbc.Nav(
            [
                dbc.NavLink([html.I(className="fas fa-home")], href="/", active="exact"),
                dbc.NavLink([html.I(className="fas fa-flask")], href="/experiment", active="exact"),
                dbc.NavLink([html.I(className="fas fa-chart-pie")], href="/result", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
