import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from pundit.interface.app import app

layout = html.Div([
    html.Div([
        html.H1('PUNDIT'),
        html.P('Welcome to the PUNDIT app!')
    ])
])
