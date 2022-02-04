import dash_core_components as dcc
import dash_html_components as html
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
FOR WHATEVER REASON CALLBACKS DON'T SEEM TO WORK WHEN 
DEFINED IN OTHER FILES, SO THEY'RE ALL PUT HERE
"""

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

"""
EXPERIMENT
"""

@app.callback(
    Output("modal-lg", "is_open"),
    Input("run-experiment", "n_clicks"),
    [State(input_id, "value") for input_id in ALL_INPUT_LIST],
)
def run_experiment(n_clicks, *values):
    from pundit.interface.apps.experiment import _run_experiment
    _run_experiment(n_clicks, *values)


"""
RESULTS
"""




if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

