import dash_bootstrap_components as dbc
from dash import html

def create_navbar():
    return dbc.Row(className="ls-navbar md-12", children=[
        dbc.Col(className="col-md-1 p-2 ps-4", children=[
            html.Img(src="assets/images/kraken.png", style={'height':'100px','width':'100px'}),
        ]),
        dbc.Col(className="col-md-11 p-2 mt-4", children=[
            html.H1("Kraken"),
        ]),
    ],)

