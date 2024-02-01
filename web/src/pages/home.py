from dash import dcc, html, register_page, Input, Output, callback, clientside_callback, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from utils.colors import colors

from components.graph import create_graph
from components.currency_dropdown import create_currency_dropdown
from components.method_dropdown import create_method_dropdown
from components.guage_dropdown import create_guage_dropdown
from components.predict_slider import create_predict_slider
from components.predict_button import create_predict_button
from components.guage import create_guage

register_page(module=__name__, path='/')

placeholder_df = pd.read_csv("src/data/placeholder_eur_pln.csv")

AVAIL_GUAGES = ['RSI', 'SMA', 'WMA', 'EMA']

layout = dbc.Container(children=[
    dcc.Store(id="currencies-store", data=None),
    dcc.Store(id="method-store", data=None),
    dcc.Store(id="predict-days-store", data=None),

    dbc.Row(className="row-12 mt-4 mb-4", children=[

        dbc.Col(className="col-8 p-0 pe-3", children=[
            dbc.Row(className="row-12 p-0 m-0", children=[
                dbc.Col(className="col-12 p-3 m-0 ls-tile", children=[
                    dcc.Graph(
                        id="graph",
                        figure=create_graph(df=placeholder_df, disabled=True, graph_type="line"),
                    ),
                ]),
            ]),
        ]),

        dbc.Col(className="col-4 p-0 ps-3", children=[
            dbc.Row(className="row-12 p-0 m-0", style={"height": "100%"}, children=[
                dbc.Col(className="col-12 p-4 ls-tile", children=[
                    dbc.Row(className="row-12 mb-4", children=[
                        dbc.Col(className="col-12 p-0 m-0", children=[
                            dbc.Row(className="row-12 p-0 m-0 mb-3", children=[
                                html.H4("Select currencies"),
                            ]),
                            dbc.Row(className="row-12 p-0 m-0 mb-2", children=[
                                dbc.Col(className="col-6", children=[
                                    create_currency_dropdown(id=1),
                                ]),
                                dbc.Col(className="col-6", children=[
                                    create_currency_dropdown(id=2),
                                ]),
                            ]),
                        ]),
                    ]),
                    dbc.Row(className="row-12 mb-4", children=[
                        dbc.Col(className="col-12 p-0 m-0", children=[
                            dbc.Row(className="row-12 p-0 m-0 mb-3", children=[
                                html.H4("Select prediction method"),
                            ]),
                            dbc.Row(className="row-12 p-0 m-0 mb-2", children=[
                                create_method_dropdown(),
                            ]),
                        ]),
                    ]),
                    dbc.Row(className="row-12 mb-4", children=[
                        dbc.Col(className="col-12 p-0 m-0", children=[
                            dbc.Row(className="row-12 p-0 m-0 mb-3", children=[
                                html.H4("Select prediction days"),
                            ]),
                            dbc.Row(className="row-12 p-0 m-0 mb-2", children=[
                                create_predict_slider(),
                            ]),
                        ]),
                    ]),
                    dbc.Row(className="row-12", children=[
                        dbc.Col(className="col-12 p-0 m-0", children=[
                            dbc.Row(className="row-12 p-0 m-0", style={"display": "flex", "justify-content": "center"}, children=[
                                create_predict_button()
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),

    ]),


    dbc.Row(className="row-12 mt-4", children=[

        dbc.Col(className="col-3 p-0 pe-4", children=[
            dbc.Row(className="row-12 p-0 m-0", children=[
                dbc.Col(className="col-12 p-3 ls-tile", children=[
                    dbc.Row(className="row-12", children=[
                        create_guage(name="RSI"),
                    ]),
                    dbc.Row(className="row-12", children=[
                        dbc.Col(className="col-4 ps-4 pe-2", style={'fontSize': '24px', 'textAlign': 'center'}, children=[
                            "RSI",
                        ]),
                        dbc.Col(className="col-8 ps-2 pe-4", children=[
                            create_guage_dropdown(id="RSI")
                        ])
                    ]),
                ]),
            ]),
        ]),

        dbc.Col(className="col-3 p-0 ps-2 pe-3", children=[
            dbc.Row(className="row-12 p-0 m-0", children=[
                dbc.Col(className="col-12 p-3 ls-tile", children=[
                    dbc.Row(className="row-12", children=[
                        create_guage(name="SMA"),
                    ]),
                    dbc.Row(className="row-12", children=[
                        dbc.Col(className="col-4 ps-4 pe-2", style={'fontSize': '24px', 'textAlign': 'center'}, children=[
                            "SMA",
                        ]),
                        dbc.Col(className="col-8 ps-2 pe-4", children=[
                            create_guage_dropdown(id="SMA")
                        ])
                    ]),
                ]),
            ]),
        ]),

        dbc.Col(className="col-3 p-0 ps-3 pe-2", children=[
            dbc.Row(className="row-12 p-0 m-0", children=[
                dbc.Col(className="col-12 p-3 ls-tile", children=[
                    dbc.Row(className="row-12", children=[
                        create_guage(name="WMA"),
                    ]),
                    dbc.Row(className="row-12", children=[
                        dbc.Col(className="col-4 ps-4 pe-2", style={'fontSize': '24px', 'textAlign': 'center'}, children=[
                            "WMA",
                        ]),
                        dbc.Col(className="col-8 ps-2 pe-4", children=[
                            create_guage_dropdown(id="WMA")
                        ])
                    ]),
                ]),
            ]),
        ]),

        dbc.Col(className="col-3 p-0 ps-4", children=[
            dbc.Row(className="row-12 p-0 m-0", children=[
                dbc.Col(className="col-12 p-3 ls-tile", children=[
                    dbc.Row(className="row-12", children=[
                        create_guage(name="EMA"),
                    ]),
                    dbc.Row(className="row-12", children=[
                        dbc.Col(className="col-4 ps-4 pe-2", style={'fontSize': '24px', 'textAlign': 'center'}, children=[
                            "EMA",
                        ]),
                        dbc.Col(className="col-8 ps-2 pe-4", children=[
                            create_guage_dropdown(id="EMA")
                        ])
                    ]),
                ]),
            ]),
        ]),

    ]),



    html.Div(id="loading-container", className="ls-loading-container", style={'display': 'none'}, children=[
        html.Div(className="ls-spinner-container", children=[
            dbc.Spinner(size="lg", color=colors["--ls-increasing-color"], id="loading-spinner", spinner_style={"width": "10rem", "height": "10rem"}),
        ]),
    ]),

    html.Div(id="toast-container", className="ls-toast-container", children=[

    ]),

    dbc.Button(
        id="predict-btn",
        className="btn-primary",
        style={'display': 'none'},
        n_clicks=0
    ),

])
