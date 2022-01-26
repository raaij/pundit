import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback_context, dcc, html
from wdo.constant import PATH_RESULTS
from wdo.gui.common.drop import dropdown1
from wdo.gui.common.navbar import navbar
from wdo.gui.common.dropmetrics import dropdown2
from wdo.gui.common.dropcombin import dropdown3
from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import Button
from wdo.gui.common.drop import display_experiment
data = pd.read_csv(PATH_RESULTS / "example.csv").reset_index()  # TODO this needs to be dynamic

def get_impression_count_grouped():
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

def get_table_summary():
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

def get_asset_summary(asset_type):
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
        dropdown1,
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
                                html.P("Test Experiment 123"),
                                className="lead"
                            )
                        ])
                    ],
                    fluid=True,
                    className="py-3",
                ),
                dbc.Row(
                    [
                        dropdown2,
                        dbc.Col(
                            get_impression_count_grouped(),
                            width=5
                        ),
                        dbc.Col(
                            get_table_summary()

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
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            get_asset_summary('header')
                        ),
                        dbc.Col(
                            get_asset_summary('description')
                        ),
                        dbc.Col(
                            get_asset_summary('image')
                        ),
                    ]
                )
            ],
            fluid=True
        )
    ],
)
