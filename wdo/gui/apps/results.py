from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash import Dash, html, Input, Output, callback_context, State
from app import app
from common.navbar import navbar
from common.drop import dropdown
from constant import PATH_EXPERIMENTS

layout = html.Div(
    children=[
        navbar,
        dbc.Container(
            children=[
                dropdown,
                dbc.Row(
                    "Experiment Name"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row("Combinations"),
                                dbc.Row("Combination 1 : Header 1 - Image 1 - Description 1"),
                                dbc.Row("Combination 2 : Header 1 - Image 1 - Description 2"),
                                dbc.Row("...")
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Row(""),
                                dbc.Row("..."),
                                dbc.Row("..."),
                                dbc.Row("...")
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row("Specific Information - Headers"),
                                dbc.Row("Header 1"),
                                dbc.Row("Header 2"),
                                dbc.Row("...")
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Row("Specific Information - Descriptions"),
                                dbc.Row("Description 1"),
                                dbc.Row("Description 2"),
                                dbc.Row("...")
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Row("Specific Information - Images"),
                                dbc.Row("Image 1"),
                                dbc.Row("Image 2"),
                                dbc.Row("...")
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    "Graph Here"
                )
            ]
        ),
    ],
)
