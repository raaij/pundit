"""
TODO:
    - Make number of inputs dynamic
"""

import json

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback_context, html

from wdo.constant import PATH_EXPERIMENTS
from wdo.experiment import Experiment
from wdo.gui.app import app
from wdo.gui.common.navbar import navbar

layout = html.Div(
    children=[
        navbar,
        dbc.Container(
            children=[
                dbc.Row(
                    [
                        dbc.Col([dbc.Row("Experiment Name")]),
                        dbc.Col(
                            [
                                dbc.Row(
                                    dbc.Input(
                                        id="input1".format("text") ,
                                        required="required",
                                        placeholder="Enter Experiment Name".format("text"),
                                    )
                                )
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row("Headers"),
                                dbc.Row(
                                    dbc.Input(
                                        id="input2".format("text"),
                                        required="required",
                                        placeholder="Header 1".format("text"),
                                    )
                                ),
                                dbc.Row(
                                    dbc.Input(
                                        id="input3".format("text"),
                                        required="required",
                                        placeholder="Header 2".format("text"),
                                    )
                                ),
                                dbc.Row(
                                    [
                                        dbc.Button(
                                            "Add Extra Input Header", id="input-header", n_clicks=0
                                        )
                                    ]
                                ),
                                html.Div(id="container-header"),
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Row("Images"),
                                dbc.Row(
                                    dbc.Input(
                                        id="input4".format("text"),
                                        required="required",
                                        placeholder="Image 1".format("text"),
                                    )
                                ),
                                dbc.Row(
                                    dbc.Input(
                                        id="input5".format("text"),
                                        required="required",
                                        placeholder="Image 2".format("text"),
                                    )
                                ),
                                dbc.Row(
                                    [
                                        dbc.Button(
                                            "Add Extra Input Image", id="input-image", n_clicks=0
                                        )
                                    ]
                                ),
                                html.Div(id="container-image"),
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row("Descriptions"),
                                dbc.Row(
                                    dbc.Input(
                                        id="input6".format("text"),
                                        required="required",
                                        placeholder="Description 1".format("text"),
                                    )
                                ),
                                dbc.Row(
                                    dbc.Input(
                                        id="input7".format("text"),
                                        required="required",
                                        placeholder="Description 2".format("text"),
                                    )
                                ),
                                dbc.Row(
                                    [
                                        dbc.Button(
                                            "Add Extra Input Description",
                                            id="input-description",
                                            n_clicks=0,
                                        )
                                    ]
                                ),
                                html.Div(id="container-description"),
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row("Accuracy"),
                                dbc.Row(
                                    dbc.Input(
                                        id="input8".format("number"),
                                        placeholder="95% by default".format("text"),
                                    )
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Row("Budget"),
                                dbc.Row(
                                    dbc.Input(
                                        id="input9".format("number"),
                                        required="required",
                                        placeholder="Enter Value".format("text"),
                                    )
                                ),
                            ]
                        ),
                        dbc.Col([dbc.Button("Run Experiment", id="run-experiment", n_clicks=0)]),
                        html.Div(id="container"),
                    ]
                ),
            ],
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Ran experiment!")),
                dbc.ModalBody("You can visit the results page to view the results."),
            ],
            id="modal-lg",
            size="lg",
            is_open=False,
        ),
    ],
)


def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(
    Output("modal-lg", "is_open"),
    Input("run-experiment", "n_clicks"),
    [State("input{}".format(i), "value") for i in range(1, 9)],
)
def run_experiment(n_clicks, *values):
    idxs = [f"input_{i}" for i in range(1, 9)]
    if n_clicks > 0:
        experiment = {idx: value for idx, value in zip(idxs, values)}
        name = experiment["input_1"]  # experiment name
        path_file = PATH_EXPERIMENTS / (name + ".json")
        with open(path_file, "w+") as fp:
            json.dump(experiment, fp)

        experiment = Experiment.from_config(path_file)
        experiment.run()
        experiment.save()
        return True
    return False
