import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, MATCH
import dash_daq as daq
from utils.colors import colors


def create_guage(name: str):
    return daq.Gauge(
        id={
            'type': 'guage',
            'index': name,
        },
        color={
            "gradient":False,
            "ranges":{
                colors["--ls-decreasing-color"]:[0,1.5],
                colors["--ls-neutral-color"]:[1.5,2.5],
                colors["--ls-increasing-color"]:[2.5,4]
            }
        },
        value=0,
        label={"label": "Default", "style": {"fontSize": "20px"}},
        max=4,
        min=0,
        size=170,
        scale={"custom": {i: {"label": f"{i}"} for i in range(5)}},
        labelPosition="top",
    )


@callback(
    Output(component_id={'type': 'guage', 'index': MATCH}, component_property='label'),
    Input(component_id={'type': 'guage', 'index': MATCH}, component_property='value'),
    prevent_initial_call=True,
)
def update_guage_label(input_value):
    label_properties = {
        0: {"label": "Strong Sell", "style": {"color": colors["--ls-decreasing-color"], "fontSize": "20px"}},
        1: {"label": "Sell", "style": {"color": colors["--ls-decreasing-color"], "fontSize": "20px"}},
        2: {"label": "Neutral", "style": {"color": colors["--ls-neutral-color"], "fontSize": "20px"}},
        3: {"label": "Buy", "style": {"color": colors["--ls-increasing-color"], "fontSize": "20px"}},
        4: {"label": "Strong Buy", "style": {"color": colors["--ls-increasing-color"], "fontSize": "20px"}},
    }
    return label_properties[input_value]
