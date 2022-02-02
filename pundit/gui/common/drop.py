import os
import dash
from pundit.gui.app import app
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
    files = os.listdir(PATH_EXPERIMENTS)
    for file1 in files:
        if file1.endswith(".json"):
            final_list.append(file1.replace(".json", ""))
    items = [dbc.DropdownMenuItem(i, id=i) for i in final_list]
    return items


dropdown1 = html.Div(
    [
        dbc.DropdownMenu(
            children=items,
            label="Choose Experiment"
        ),
        html.P(id="drop-experiment", className="mt-3"),
    ],
    id="menu"
)

@app.callback(
    Output("drop-experiment", "children"),
    [Input(i, "n_clicks") for i in final_list],
    prevent_initial_callbacks=True
)


def display_experiment(*args):
    ctx = dash.callback_context
    if ctx.triggered:
        fix_final_list()
        button_id.append(ctx.triggered[0]["prop_id"].split(".")[0])
        return True
    else:
        return 'You have selected "None"'
