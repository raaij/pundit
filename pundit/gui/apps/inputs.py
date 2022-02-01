import json

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback_context, html

from pundit.constant import PATH_EXPERIMENTS
from pundit.experiment import Experiment
from pundit.gui.app import app
from pundit.gui.common.navbar import navbar

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
                                        id="input2".format("number"),
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
                                        id="input3".format("number"),
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
                                        id="input4".format("number"),
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
                                dbc.Row("Accuracy"),
                                dbc.Row(
                                    dbc.Input(
                                        id="input5".format("number"),
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
                                        id="input6".format("number"),
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
    [State("input{}".format(i), "value") for i in range(1, 7)],
)
def run_experiment(n_clicks, *values):
    idxs = [f"input_{i}" for i in range(1, 7)]
    experiment = {idx: value for idx, value in zip(idxs, values)}
    numb_req = [1, 2, 3, 4, 6]
    counter = 0
    for numb in numb_req:
        if experiment[("input_" + str(numb))] is not None and experiment[("input_" + str(numb))] != "":
            counter += 1
    if n_clicks > 0 and counter == 5:
        name = experiment["input_1"]  # experiment name
        path_file = PATH_EXPERIMENTS / (name + ".json")
        with open(path_file, "w+") as fp:
            json.dump(experiment, fp)

        experiment = Experiment.from_config(path_file)
        experiment.run()
        experiment.save()
        return True
    return False

