import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output

from utils.colors import colors

selected_style = {
    "color": colors["--ls-increasing-color"],
    "font-weight": "bold"
}

not_selected_style = {
    "color": colors["--ls-text-color"],
    "font-weight": "normal"
}

marks = {i: {"label": f"{i}", "style": selected_style} for i in range(8)}


def create_predict_slider():
    return dcc.Slider(
        id='predict_slider',
        min=1,
        max=7,
        step=1,
        value=1,
        marks=marks
    )

@callback(
    Output(component_id='predict_slider', component_property='marks'),
    Input(component_id='predict_slider', component_property='value'),
)
def highlight_day_number(input_value):
    for day_no, props in marks.items():
        if input_value >= day_no: props["style"] = selected_style
        else: props["style"] = not_selected_style
    return marks


@callback(
    Output(component_id='predict-days-store', component_property='data'),
    Input(component_id='predict_slider', component_property='value'),
)
def store_day_number(input_value):
    return input_value