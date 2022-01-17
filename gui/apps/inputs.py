import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, callback_context

from common.navbar import navbar

layout = html.Div(
    children=[
        navbar,
        dbc.Container(
            children=[
                dbc.Row(
                    [
                        dbc.Col([dbc.Row("Experiment Name")]),
                        dbc.Col([dbc.Row(dbc.Input(id="Input-Exp-Name".format("text"), placeholder="Enter Experiment Name".format("text")))]),
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
                        dbc.Col([dbc.Button("Run Experiment", id="Exp-btn", n_clicks=0)]),
                        html.Div(id="container")
                    ]
                ),
            ],
        ),
    ],
)

def Json_saved(input1, input2, input3, input4, input5, input6, n_clicks):
    if n_clicks:
        return json.dumps(input1, input2, input3, input4, input5, input6)

@callback(
    Output("container", "children"),
    Input("Exp-btn", "n_clicks")
)
def Create_file(input1, input2, input3, input4, input5, input6, button):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'Exp-btn' in changed_id:
        f = open(r"C:\Users\atsia\PycharmProjects\textfile.txt", "w")
        f.write(json.dumps(input1, input2, input3, input4, input5, input6))
        f.close()
