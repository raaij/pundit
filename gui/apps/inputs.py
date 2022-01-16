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
                                dbc.Row(dbc.Input(id="input1".format("text"), placeholder="Header 1".format("text"))),
                                dbc.Row(dbc.Input(id="input2".format("text"), placeholder="Header 2".format("text"))),
                                dbc.Row("..."),
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Row("Images"),
                                dbc.Row(dbc.Input(id="input3".format("text"), placeholder="Image 1".format("text"))),
                                dbc.Row(dbc.Input(id="input4".format("text"), placeholder="Image 2".format("text"))),
                                dbc.Row("...")
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row("Descriptions"),
                                dbc.Row(dbc.Input(id="input5".format("text"), placeholder="Description 1".format("text"))),
                                dbc.Row(dbc.Input(id="input6".format("text"), placeholder="Description 2".format("text"))),
                                dbc.Row("...")
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row("Accuracy"),
                                dbc.Row(dbc.Input(id="input7".format("number"), placeholder="95% by default".format("text")))
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Row("Confidence"),
                                dbc.Row(dbc.Input(id="input8".format("number"), placeholder="Enter Value".format("text")))
                            ]
                        ),
                        dbc.Col([dbc.Button("Run Experiment", n_clicks=0)]),
                    ]
                ),
            ],
        ),
    ],
)

def Json_saved(input1, input2, input3, input4, input5, input6, n_clicks):
    if n_clicks:
        return json.dumps(input1, input2, input3, input4, input5, input6)
