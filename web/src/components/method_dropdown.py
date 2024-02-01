import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output

dropdown_style = {
    "border-radius": "10px",
    "border-color": "#42eb91",
    "border-width": "2px",
}

option_list = [
    "LSTM",
]

def create_method_dropdown():
    return dcc.Dropdown(
        id="method_dropdown",
        style=dropdown_style,
        options=option_list,
        placeholder="Method",
    )


@callback(
    Output(component_id='method-store', component_property='data'),
    Input(component_id='method_dropdown', component_property='value'),
    prevent_initial_call=True,
)
def store_selected_currencies(input_value):
    return input_value