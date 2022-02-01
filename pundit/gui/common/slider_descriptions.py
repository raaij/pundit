from pundit.gui.app import app
from dash import Input, Output, html, dcc

sliderdescriptions = html.Div([
    dcc.Slider(
        id='descriptions-slider',
        min=1,
        max=10,
        step=1,
        value=1,
        marks={
            1: '1 Description',
            5: '5 Descriptions',
            10: '10 Descriptions'
        },
    ),
    html.Div(id='slider-output-descriptions')
])

@app.callback(
    Output('slider-output-descriptions', 'children'),
    [Input('descriptions-slider', 'value')]
)

def update_output(value):
    return 'You have selected "{}" descriptions'.format(value)