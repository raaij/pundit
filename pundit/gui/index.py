from dash import dcc, html
from dash.dependencies import Input, Output

from pundit.gui.app import app
from pundit.gui.apps import inputs, results

app.layout = html.Div([dcc.Location(id="url", refresh=False), html.Div(id="page-content")])
server = app.server

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        return inputs.layout
    elif pathname == "/results":
        return results.layout
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(debug=True)
