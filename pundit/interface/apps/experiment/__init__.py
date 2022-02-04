import json

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback_context, html

# from pundit.constant import PATH_EXPERIMENTS
# from pundit.experiment import Experiment
# from pundit.gui.app import app
# from pundit.gui.common.navbar import navbar

from pundit.constant import PATH_DATA_INPUT, PATH_DATA_RESULT
from pundit.core.experiment import Experiment
from .input import *


layout = html.Div(
    children=[
        dbc.Container(
            children=[
                dbc.Row(
                    [
                        dbc.Col([dbc.Row("Experiment Name")]),
                        dbc.Col(
                            [
                                dbc.Row(
                                    dbc.Input(
                                        id=INPUT_EXPERIMENT_NAME,
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
                                        id=INPUT_HEADER_COUNT,
                                        required="required",
                                        placeholder="Number of Headers".format("text"),
                                    ),
                                ),
                                html.Div(id="container-header")
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Row("Images"),
                                dbc.Row(
                                    dbc.Input(
                                        id=INPUT_IMAGE_COUNT,
                                        required="required",
                                        placeholder="Number of Images".format("text"),
                                    ),
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
                                        id=INPUT_DESCRIPTION_COUNT,
                                        required="required",
                                        placeholder="Number of Descriptions".format("text"),
                                    )
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
                                dbc.Row("Confidence (%)"),
                                dbc.Row(
                                    dbc.Input(
                                        id=INPUT_CONFIDENCE,
                                        value="95",
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
                                        id=INPUT_BUDGET,
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
    [State(input_id, "value") for input_id in ALL_INPUT_LIST],
)

def _run_experiment(n_clicks, *values):
    experiment = {idx: value for idx, value in zip(ALL_INPUT_LIST, values)}

    if n_clicks > 0:
        name = experiment[INPUT_EXPERIMENT_NAME]  # experiment name
        _initialize_experiment_directories(name)
        path_file = PATH_DATA_INPUT / name / "input.json"

        with open(path_file, "w+") as fp:
            json.dump(experiment, fp)

        experiment = Experiment.from_input(path_file)
        experiment.configure()
        experiment.run()
        experiment.save()
        return True
    return False

def _initialize_experiment_directories(name):
    for directory in [
        PATH_DATA_INPUT / name,
        PATH_DATA_RESULT / name,
        # TODO: Static directory
    ]:
        directory.mkdir(exist_ok=True)
