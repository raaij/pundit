from dash import html, dcc
from dash.dependencies import Input, Output, State

from pundit.interface.app import app
from pundit.interface.apps import experiment, home, result
from pundit.interface.common.sidebar import sidebar
from pundit.interface.common.content import content
from pundit.interface.apps.experiment import ALL_INPUT_LIST

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    content,
    sidebar,
])


"""
MAIN
"""

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/result':
        return result.layout
    elif pathname == '/experiment':
        return experiment.layout
    else:
        return '404'





if __name__ == '__main__':
    app.run_server(debug=True)
