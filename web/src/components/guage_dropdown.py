import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output

dropdown_style = {
    "border-radius": "10px",
    "border-color": "#42eb91",
    "border-width": "2px",
}

option_list = [
    "10 days",
    "20 days",
    "50 days",
    "100 days",
    "200 days"
]

def create_guage_dropdown(id: str):
    return dcc.Dropdown(
        id={'type': 'dropdown', 'index': id},
        style=dropdown_style,
        options=option_list,
        value=option_list[0],
        clearable=False,
    )