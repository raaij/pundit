import os
import dash
from pundit.gui.app import app
from pundit.gui.apps import inputs
import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc
from pundit.constant import PATH_EXPERIMENTS


files = os.listdir(PATH_EXPERIMENTS)
final_list = []
items = []
button_id = []
for file in files:
    if file.endswith(".json"):
        final_list.append(file.replace(".json", ""))
items = [dbc.DropdownMenuItem(i, id=i) for i in final_list]

def fix_final_list():
    fixed_list = []
    file_list = os.listdir(PATH_EXPERIMENTS)
    for file_1 in file_list:
        if file_1.endswith(".json"):
            fixed_list.append(file_1.replace(".json", ""))
    return fixed_list

def button_list(items):
    final_list = []
    files = os.listdir(PATH_EXPERIMENTS)
    for file in files:
        if file.endswith(".json"):
            final_list.append(file.replace(".json", ""))
    items = [dbc.DropdownMenuItem(i, id=i) for i in fix_final_list()]

    return items


dropdown1 = html.Div(
    [
        dbc.DropdownMenu(
            children=items,
            label="Choose Experiment",
            id="labels"
        ),
        html.P(id="drop-experiment", className="mt-3"),
    ],
    id="menu"
)

@app.callback(
    Output("drop-experiment", "children"),
    [Input(i, "n_clicks") for i in fix_final_list()],
)

def display_experiment(*args):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id.append(ctx.triggered[0]["prop_id"].split(".")[0])
        return True
    else:
        return 'You have selected "None"'

@app.callback(
    Output("labels", "children"),
    Input("drop-experiment", "children")
)

def display_experiment(children, *args):
    if children is not None:
        return button_list(items)
    else:
        return items
