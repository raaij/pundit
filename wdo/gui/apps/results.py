import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback_context, dcc, html

from wdo.gui.common.drop import dropdown
from wdo.gui.common.navbar import navbar

layout = html.Div(
    children=[
        navbar,
        dbc.Container(
            children=[
                dropdown,
                dbc.Row("Experiment Name"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row("Combinations"),
                                dbc.Row("Combination 1 : Header 1 - Image 1 - Description 1"),
                                dbc.Row("Combination 2 : Header 1 - Image 1 - Description 2"),
                                dbc.Row("..."),
                            ]
                        ),
                        dbc.Col([dbc.Row(""), dbc.Row("..."), dbc.Row("..."), dbc.Row("...")]),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row("Specific Information - Headers"),
                                dbc.Row("Header 1"),
                                dbc.Row("Header 2"),
                                dbc.Row("..."),
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Row("Specific Information - Descriptions"),
                                dbc.Row("Description 1"),
                                dbc.Row("Description 2"),
                                dbc.Row("..."),
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Row("Specific Information - Images"),
                                dbc.Row("Image 1"),
                                dbc.Row("Image 2"),
                                dbc.Row("..."),
                            ]
                        ),
                    ]
                ),
                dbc.Row("Graph Here"),
            ]
        ),
    ],
)
