import dash_core_components as dcc
import dash_html_components as html
from app import app
from apps import inputs, results
from dash.dependencies import Input, Output

app.layout = html.Div([dcc.Location(id="url", refresh=False), html.Div(id="page-content")])


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
