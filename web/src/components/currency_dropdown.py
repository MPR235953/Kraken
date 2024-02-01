import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate

dropdown_style = {
    "border-radius": "10px",
    "border-color": "#42eb91",
    "border-width": "2px",
}

dropdown_item_style = {
    'align-items': 'center',
    'justify-content': 'center',
}

currency_name_style = {
    'font-size': 15,
    'padding-left': 10,
}

option_list = [
    {
        "label": html.Span(children=[
                html.I(className="flag flag-poland"),
                html.Span("PLN", style=currency_name_style),
            ], style=dropdown_item_style
        ),
        "value": "PLN",
    },
    {
        "label": html.Span(children=[
                html.I(className="flag flag-european-union"),
                html.Span("EUR", style=currency_name_style),
            ], style=dropdown_item_style
        ),
        "value": "EUR",
    },
    {
        "label": html.Span(children=[
                html.I(className="flag flag-united-states"),
                html.Span("USD", style=currency_name_style),
            ], style=dropdown_item_style
        ),
        "value": "USD",
    },
]

def create_currency_dropdown(id: int = 1):
    return dcc.Dropdown(
        id=f"currency_dropdown_{id}",
        style=dropdown_style,
        options=option_list,
        placeholder=f"Currency {id}",
    )

@callback(
    [
        Output(component_id='currency_dropdown_1', component_property='options'),
        Output(component_id='currency_dropdown_2', component_property='options'),
    ],
    [
        Input(component_id='currency_dropdown_1', component_property='value'),
        Input(component_id='currency_dropdown_2', component_property='value'),
    ],
    prevent_initial_call=True,
)
def prevent_currency_doubles(input_value_1, input_value_2):
    new_options_1 = [option for option in option_list if option["value"] != input_value_2]
    new_options_2 = [option for option in option_list if option["value"] != input_value_1]
    return new_options_1, new_options_2


@callback(
    Output(component_id='currencies-store', component_property='data'),
    [
        Input(component_id='currency_dropdown_1', component_property='value'),
        Input(component_id='currency_dropdown_2', component_property='value'),
    ],
    prevent_initial_call=True,
)
def store_selected_currencies(input_value_1, input_value_2):
    if not input_value_1 or not input_value_2:
        return None
    else:
        return [input_value_1, input_value_2]