import dash_bootstrap_components as dbc
from dash import html

from common.navbar import navbar

layout = html.Div(
    children=[
        navbar,
        dbc.Container(
            children=[
                dbc.Row(
                    [
                        dbc.Col([dbc.Row("Experiment Name")]),
                        dbc.Col([dbc.Row("Cool experiment 112")]),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row("Headers"),
                                dbc.Row("Header 1"),
                                dbc.Row("Header 2"),
                                dbc.Row("..."),
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Row("Descriptions"),
                                dbc.Row("Description 1"),
                                dbc.Row("Description 2"),
                                dbc.Row("..."),
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row("Images"),
                                dbc.Row("Image 1"),
                                dbc.Row("Image 2"),
                                dbc.Row("..."),
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col([dbc.Row("Accuracy"), dbc.Row("Value")]),
                        dbc.Col([dbc.Row("Confidence"), dbc.Row("Value")]),
                        dbc.Col([dbc.Button("Run Experiment")]),
                    ]
                ),
            ],
        ),
    ],
)
