import dash
import dash_bootstrap_components as dbc
import plotly.io as pio

pio.templates.default = "simple_white"

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.PULSE,
        "https://fonts.googleapis.com/css2?family=Work+Sans&display=swap",
        dbc.icons.FONT_AWESOME
    ],
    suppress_callback_exceptions=True
)

# app.css.config.serve_locally = True

server = app.server
