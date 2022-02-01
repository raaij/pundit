import os
import dash
from pundit.gui.app import app
import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc
from pundit.constant import PATH_EXPERIMENTS

files = os.listdir(PATH_EXPERIMENTS)
final_list = []
for file in files:
    if file.endswith(".json"):
        final_list.append(file.replace(".json", ""))
items = [dbc.DropdownMenuItem(i, id=i) for i in final_list]


dropdown1 = html.Div(
    [
        dbc.DropdownMenu(
            children=items,
            label="Choose Experiment"
        ),
        html.P(id="drop-experiment", className="mt-3"),
    ]
)
@app.callback(
    Output("drop-experiment", "children"),
    [Input(i, "n_clicks") for i in final_list]
)


def display_experiment(*args):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        return "The Experiment is: " + button_id
