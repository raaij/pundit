import os
import dash_bootstrap_components as dbc
from dash import Input, Output, html
from pundit.gui.app import app
from dash import Dash, Input, Output, State, callback_context, dcc, html

dropdown3 = html.Div([
    dcc.Dropdown(
        id='combin-dropdown',
        options = [
            {'label': 'Top 10 combinations', 'value': 'Top10'},
            {'label': 'ALL', 'value': 'all'},
        ],
        placeholder="Choose Combinations for graph",
        searchable=False
    ),
    html.Div(id='combin-container')
])

@app.callback(
    Output('combin-container', 'children'),
    Input('combin-dropdown', 'value')
)

def display_metric(value):
    return 'You have selected "{}"'.format(value)
