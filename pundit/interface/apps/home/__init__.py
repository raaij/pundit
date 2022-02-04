import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output

from pundit.interface.app import app

layout = html.Div([
    html.Div([
        html.H1('PUNDIT'),
        html.P('Welcome to the PUNDIT app!')
    ])
])
