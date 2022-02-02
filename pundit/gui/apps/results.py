import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback_context, dcc, html, exceptions
from dash.exceptions import PreventUpdate

from pundit.gui.app import app
from pundit.constant import PATH_RESULTS
from pundit.gui.common import drop
from pundit.gui.common.navbar import navbar
from pundit.gui.common.dropmetrics import dropdown2
from pundit.gui.common.dropcombin import dropdown3
from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import Button
# from pundit.gui.common.drop import display_experiment
from pundit.gui.common import drop

def fix_data(experiment=None):
    if not experiment:
        experiment = 'example'
    data = pd.read_csv(PATH_RESULTS / (experiment + '.csv')).reset_index()
    # if len(drop.button_id) == 0:
    #     data = pd.read_csv(PATH_RESULTS / (drop.final_list[0] + ".csv")).reset_index()  # TODO this needs to be dynamic
    #     return data
    # else:
    #     data = pd.read_csv(PATH_RESULTS / (drop.button_id[len(drop.button_id)-1]+".csv")).reset_index()# TODO this needs to be dynamic
    #     get_impression_count_grouped(data)
    #     get_table_summary(data)
    #     return data
    return data

def get_impression_count_grouped(data):
    data['hundred'] = np.round(data.time, -2)
    dff = data.groupby(['hundred', 'arm'])[['reward']].count().reset_index()
    dff.columns = ['idx', 'arm', 'count']
    dff['cumcount'] = dff.groupby(['arm'])['count'].cumsum()
    fig = px.area(dff, x="idx", y="count", color="arm")
    return dcc.Graph(
        id='grouped-impression-count',
        figure=fig,
        config={
            'displayModeBar': False
        }
    )

def get_table_summary(data):
    import itertools
    dff = data.groupby('arm').agg({'reward': ['count', 'sum']})
    dff = dff.reset_index()
    dff.columns = ['combination', 'impressions', 'clicks']
    meta = pd.DataFrame(list(itertools.product(range(2), range(2), range(2))))
    dff['header'] = meta[0]
    dff['description'] = meta[1]
    dff['image'] = meta[2]
    dff = dff[[
        'combination', 'header', 'description', 'image', 'impressions', 'clicks',
    ]]

    # TODO: Fix this
    dff['ctr (%)'] = (100 * np.round(dff['clicks'] / dff['impressions'], 4)).astype(str).apply(lambda x: x[:4])

    return dbc.Table.from_dataframe(dff, hover=True)

def get_asset_summary(asset_type, data):
    import itertools
    dff = data.groupby('arm').agg({'reward': ['count', 'sum']})
    dff = dff.reset_index()
    dff.columns = ['combination', 'impressions', 'clicks']
    meta = pd.DataFrame(list(itertools.product(range(2), range(2), range(2))))
    dff['header'] = meta[0]
    dff['description'] = meta[1]
    dff['image'] = meta[2]
    dff = dff[[
        'combination', 'header', 'description', 'image', 'impressions', 'clicks',
    ]]
    dff = dff.groupby(asset_type)[['impressions', 'clicks']].sum().reset_index()
    dff[asset_type] = f'{asset_type.title()} ' + dff[asset_type].apply(str)
    dff['ctr (%)'] = (100 * np.round(dff['clicks'] / dff['impressions'], 4)).astype(str).apply(lambda x: x[:4])
    return dbc.Table.from_dataframe(dff, hover=True)


layout = html.Div(
    children=[
        navbar,
        drop.dropdown1,
        dbc.Container(
            children=[
                dbc.Container(
                    [
                        dbc.Row([
                            dbc.Col(
                                html.P("Experiment:"),
                                className="lead",
                                width=1
                            ),
                            dbc.Col(
                                html.P(drop.final_list[len(drop.final_list)-1]),
                                className="lead"
                            )
                        ])
                    ],
                    fluid=True,
                    className="py-3",
                    id="header"
                ),
                dbc.Row(
                    [
                        dropdown2,
                        dbc.Col(
                            children=get_impression_count_grouped(fix_data()),
                            id='graph',
                            width=5
                        ),
                        dbc.Col(
                            get_table_summary(fix_data()),
                            id='table'
                        ),
                        dbc.Col(
                            [
                                dbc.Button(
                                    "Download ALL Combinations",
                                    download="example.csv",
                                    color="primary",
                                    external_link=True,
                                ),
                                dropdown3
                            ]
                        )
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            get_asset_summary('header', fix_data()),
                            id='table2'
                        ),
                        dbc.Col(
                            get_asset_summary('description', fix_data()),
                            id='table3'
                        ),
                        dbc.Col(
                            get_asset_summary('image', fix_data()),
                            id='table4'
                        ),
                    ]
                )
            ],
            fluid=True
        ),
    ],
)


@app.callback(
    Output("header", "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def display_header(value):
    ctx = callback_context
    if value is not None:
        return "The Experiment is: " + value

@app.callback(
    Output("graph", "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def display_graph(value):
    return get_impression_count_grouped(fix_data(value))

@app.callback(
    Output("table", "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def display_table(value):
    return get_table_summary(fix_data(value))

@app.callback(
    Output("table2", "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def display_table2(value):
    return get_asset_summary('header', fix_data(value))

@app.callback(
    Output("table3", "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def display_table3(value):
    return get_asset_summary('description', fix_data(value))

@app.callback(
    Output("table4", "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def display_table4(value):
    get_asset_summary('image', fix_data(value))

from pundit.constant import PATH_EXPERIMENTS
import os


@app.callback(
    [Output('result-dropdown', 'options'), Output('result-dropdown', 'value')],
    [Input("url", "href")]
)
def update_date_dropdown(input_):
    if input_ is None:
        raise PreventUpdate

    files = reversed(
        sorted(PATH_EXPERIMENTS.iterdir(), key=os.path.getmtime)
    )
    files = [file.name for file in files]

    result = []
    for file in files:
        if file.endswith(".json"):
            item = file.replace('.json', '')
            result.append({
                'label': item,
                'value': item
            })

    return result, result[0]['value']
