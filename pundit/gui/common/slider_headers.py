from pundit.gui.app import app
from dash import Input, Output, html, dcc

sliderheaders = html.Div([
    dcc.Slider(
        id='headers-slider',
        min=1,
        max=10,
        step=1,
        value=1,
        marks={
            1: '1 header',
            5: '5 headers',
            10: '10 headers'
        },
    ),
    html.Div(id='slider-output-headers')
])

@app.callback(
    Output('slider-output-headers', 'children'),
    [Input('headers-slider', 'value')]
)

def update_output(value):
    return 'You have selected "{}" headers'.format(value)