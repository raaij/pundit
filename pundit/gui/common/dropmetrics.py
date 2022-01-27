import os
import dash_bootstrap_components as dbc
from dash import Input, Output, html
from pundit.gui.app import app
from dash import Dash, Input, Output, State, callback_context, dcc, html


dropdown2 = html.Div([
    dcc.Dropdown(
        id='metrics-dropdown',
        options = [
            {'label': 'impressions', 'value': 'impressions'},
            {'label': 'clicks', 'value': 'clicks'},
            {'label': 'ctr', 'value': 'click through rate (%)'}
        ],
        placeholder="Choose Metric",
        searchable=False
    ),
    html.Div(id='output-container')
])

@app.callback(
    Output('output-container', 'children'),
    Input('metrics-dropdown', 'value')
)

def display_metric(value):
    return 'You have selected "{}"'.format(value)
