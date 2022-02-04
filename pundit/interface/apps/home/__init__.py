import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output

from pundit.interface.app import app

layout = html.Div([
    html.Div([
        html.H1('PUNDIT'),
        html.H2('decision support system for website design optimization'),
        html.P('Welcome to the PUNDIT app!'),
        html.P('Go to Input Page to insert values or to Result Page to view the results!')
    ])
])
