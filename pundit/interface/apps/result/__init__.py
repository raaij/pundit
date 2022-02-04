import itertools

from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import time
import numpy as np
import re
import os
from copy import copy
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from pundit.interface.app import app
from pundit.constant import PATH_DATA_RESULT


def reload_data(experiment=None):
    if not experiment:
        experiment = 'example'
    data = pd.read_csv(
        PATH_DATA_RESULT / experiment / 'result.csv'
    ).reset_index()
    return data


layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("RESULTS"),
        dcc.Dropdown(
            id='result-dropdown',
            options=[],
            value='Name'
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Summary", tab_id="summary"),
                            dbc.Tab(label="Assets", tab_id="assets"),
                            dbc.Tab(label="Comparison", tab_id="comparison"),
                        ],
                        id="tabs",
                        active_tab="summary",
                    ),
                    width=10
                ),
                dbc.Col(
                    dbc.Button('Download Data'),
                    className="d-flex justify-content-end"
                ),
            ],
        ),
        dbc.Container(id="tab-content", fluid=True),
    ],
    fluid=True
)

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab:
        if active_tab == "summary":
            return get_summary()
        if active_tab == "assets":
            return get_assets()
    return "No tab selected"


def get_summary():
    return [
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Row(
                    id='metric-aggregates-summary',
                    children=get_metric_aggregates_summary(reload_data())
                ),
                dbc.Row(
                    id='graph-summary',
                    children=get_graph_summary(reload_data())
                )
            ]),
            dbc.Col([
                dbc.Row(
                    id='best-combination-card-summary',
                    children=get_best_combination_card_summary(reload_data())
                ),
                dbc.Row(
                    id='top-10-table-summary',
                    children=get_top_10_table_summary(reload_data())
                )
            ])
        ])
    ]
def get_assets():
    return [
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Row(
                    id='asset_headers',
                    children=get_asset_summary('header', reload_data())
                ),
                dbc.Row(
                    id='asset_description',
                    children=get_asset_summary('description', reload_data())
                ),
                dbc.Row(
                    id='asset_image',
                    children=get_asset_summary('image', reload_data())
                )
            ])
        ])
    ]
# @app.callback(Output("store", "data"), [Input("button", "n_clicks")])
# def generate_graphs(n):
#     """
#     This callback generates three simple graphs from random data.
#     """
#     if not n:
#         # generate empty graphs when app loads
#         return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}
#
#     # simulate expensive graph generation process
#     time.sleep(2)
#
#     # generate 100 multivariate normal samples
#     data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)
#
#     scatter = go.Figure(
#         data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
#     )
#     hist_1 = go.Figure(data=[go.Histogram(x=data[:, 0])])
#     hist_2 = go.Figure(data=[go.Histogram(x=data[:, 1])])
#
#     # save figures in a dictionary for sending to the dcc.Store
#     return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}
#
def get_data_head(name, data):
    df_header = data.groupby(name).agg({'reward': ['sum', 'count']}).reset_index()
    return df_header

def get_top_10_table_summary(data):
    dff = data.groupby('action').agg({
        'reward': ['sum', 'count']
    }).reset_index()
    meta = pd.DataFrame(list(itertools.product(range(get_data_head('header', data)['header'].max()+1), range(get_data_head('description', data)['description'].max()+1), range(get_data_head('image', data)['image'].max()+1))))
    dff['header'] = meta[0]
    dff['description'] = meta[1]
    dff['image'] = meta[2]
    dff.columns = ['action','clicks', 'impressions', 'header', 'description', 'image']
    dff['ctr'] = np.round(100.0 * (dff['clicks'] / dff['impressions']), 2)
    dff = dff.sort_values('ctr', ascending=False)[:10]
    dff = dff[[
        'action', 'header', 'description', 'image', 'impressions', 'clicks','ctr'
    ]]
    dff.columns = [
        'Combination',
        'header',
        'description',
        'image',
        'Impressions',
        'Clicks',
        'Click-Through Rate (%)'
    ]
    table = dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)
    return table

def get_asset_summary(asset_type, data):
    import itertools
    dff = data.groupby('action').agg({'reward': ['sum', 'count']})
    dff = dff.reset_index()
    dff.columns = ['combination','clicks', 'impressions']
    meta = pd.DataFrame(list(itertools.product(range(get_data_head('header', data)['header'].max()+1), range(get_data_head('description', data)['description'].max()+1), range(get_data_head('image', data)['image'].max()+1))))
    dff['header'] = meta[0]
    dff['description'] = meta[1]
    dff['image'] = meta[2]
    dff = dff[[
        'combination', 'header', 'description', 'image', 'impressions', 'clicks',
    ]]
    dff = dff.groupby(asset_type)[['impressions', 'clicks']].sum().reset_index()
    dff[asset_type] = f'{asset_type.title()} ' + dff[asset_type].apply(str)
    dff['ctr'] = np.round(100.0 * (dff['clicks'] / dff['impressions']), 2)
    dff = dff.sort_values('ctr', ascending=False)
    return dbc.Table.from_dataframe(dff, hover=True)

def get_graph_summary(data):
    import random
    random.seed(12345)

    dff = copy(data)
    t = 1
    views = 0
    day = []
    total_views = data['t'].max()

    while views < total_views:
        day_views = np.ceil(random.gauss(400, 30))
        day_views = min(day_views, np.abs(total_views - views))
        day += [t for _ in range(int(day_views))]
        t += 1
        views += day_views

    dff['day'] = day
    dff = dff.groupby('day').agg({'reward': ['count', 'sum']}).reset_index()
    dff.columns = ['t', 'impressions', 'clicks']
    dff['ctr'] = 100.0 * (dff['clicks'] / dff['impressions'])
    dff = dff.iloc[:-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dff['t'],
        y=dff['impressions'],
        name="impressions",
        marker_color=px.colors.qualitative.Prism[1]
    ))

    fig.add_trace(go.Scatter(
        x=dff['t'],
        y=dff['clicks'],
        name="clicks",
        yaxis="y2",
        marker_color=px.colors.qualitative.Prism[5]
    ))

    fig.add_trace(go.Scatter(
        x=dff['t'],
        y=dff['ctr'],
        name="ctr",
        yaxis="y3",
        marker_color=px.colors.qualitative.Prism[8]
    ))

    # Create axis objects
    fig.update_layout(
                xaxis=dict(
            autorange=True,
            rangeslider=dict(
                autorange=True,
            )),
        yaxis=dict(
            title="impressions",
            visible=False,
            range=[dff['impressions'].min()*0.5, dff['impressions'].max()*1.1]
        ),
        yaxis2=dict(
            title="clicks",
            anchor="free",
            overlaying="y",
            side="left",
            position=0.15,
            visible=False,
            range=[dff['clicks'].min()*0.5, dff['clicks'].max()*1.1]
        ),
        yaxis3=dict(
            title="ctr",
            anchor="x",
            overlaying="y",
            side="right",
            visible=False,
            range=[dff['ctr'].min()*0.5, dff['ctr'].max()*1.1]
        ),
    )
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    # Update layout properties
    fig.update_layout(
        showlegend=False,
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=20),
        height=400,
        xaxis_title='time'
    )

    return dcc.Graph(
        figure=fig,
        config={
            'displayModeBar': False
        }
    )


def get_best_combination_card_summary(data):
    # Get the best combination
    dff = copy(data)
    dff = data.groupby('action').agg({
        'reward': ['sum', 'count']
    }).reset_index()
    dff.columns = ['action', 'clicks', 'impressions']
    dff['ctr'] = np.round(100.0 * (dff['clicks'] / dff['impressions']), 2)
    dff = dff.sort_values('ctr', ascending=False)[:10]
    best = dff['action'].values[0]

    # Get confidence
    confidence = data[data['action'] == best]['B_action'].values[-1]
    confidence = round(100 * (1 - confidence), 2)

    return dbc.Card(
        dbc.CardBody([
            html.H3("The best combination identified is:"),
            html.H1(f"Combination {best}"),
            html.H4(f"With confidence {confidence}%")
        ]),
        className="mb-3",
    )

def get_metric_aggregates_summary(data):
    impressions = len(data['action'])
    clicks = data['reward'].sum()
    ctr = 100.0 * clicks / impressions

    return [
        dbc.Col(
            html.Div(
                dbc.Button(
                    [
                        html.P(metric['name']),
                        html.H3(metric['value'])
                    ],
                    active=metric['active'],
                    className="me-1",
                    size="lg",
                    style={
                        "background-color": metric['color']
                    }
                ),
                className="d-grid gap-2",
            )
        )
        for metric in [
        {
            'name': 'Impressions',
            'value': f'{round(impressions / 1_000, 1)}K',
            'active': False,
            'color': px.colors.qualitative.Prism[1]
        },
        {
            'name': 'Clicks',
            'value': f'{clicks}',
            'active': False,
            'color': px.colors.qualitative.Prism[5]
        },
        {
            'name': 'Click-Through Rate',
            'value': f'{round(ctr, 1)}%',
            'active': False,
            'color': px.colors.qualitative.Prism[8]
        },
    ]
    ]

@app.callback(
    [Output('result-dropdown', 'options'), Output('result-dropdown', 'value')],
    [Input("url", "href")]
)
def update_date_dropdown(input_):
    if input_ is None:
        raise PreventUpdate

    files = reversed(
        sorted(PATH_DATA_RESULT.iterdir(), key=os.path.getmtime)
    )

    result = []
    for item in files:
        if item.is_dir():
            result.append({
                'label': item.name,
                'value': item.name
            })

    return result, result[0]['value']

@app.callback(
    Output("graph-summary", "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def update_graph_summary(value):
    return get_graph_summary(reload_data(value))

@app.callback(
    Output("top-10-table-summary", "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def update_top_10_table_summary(value):
    return get_top_10_table_summary(reload_data(value))

@app.callback(
    Output('best-combination-card-summary', "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def update_best_combination_card_summary(value):
    return get_best_combination_card_summary(reload_data(value))

@app.callback(
    Output('metric-aggregates-summary', "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def update_metric_aggregates_summary(value):
    return get_metric_aggregates_summary(reload_data(value))

@app.callback(
    Output('asset_headers', "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def update_asset_header(value):
    return get_asset_summary('header', reload_data(value))

@app.callback(
    Output('asset_description', "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def update_asset_description(value):
    return get_asset_summary('description', reload_data(value))

@app.callback(
    Output('asset_image', "children"),
    Input('result-dropdown', 'value'),
    prevent_initial_calls=True
)
def update_asset_image(value):
    return get_asset_summary('image', reload_data(value))
