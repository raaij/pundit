from pundit.gui.app import app
from dash import Input, Output, html, dcc

sliderimages = html.Div([
    dcc.Slider(
        id='images-slider',
        min=1,
        max=10,
        step=1,
        value=1,
        marks={
            1: '1 image',
            5: '5 images',
            10: '10 images',
        },
    ),
    html.Div(id='slider-output-images')
])

@app.callback(
    Output('slider-output-images', 'children'),
    [Input('images-slider', 'value')]
)

def update_output(value):
    return 'You have selected "{}" images'.format(value)