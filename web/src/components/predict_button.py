import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
import numpy as np
from dash.exceptions import PreventUpdate
from utils.colors import colors
import pandas as pd
from datetime import datetime, timedelta
from components.graph import create_graph
from components.toast import create_toast
from utils import forecaster, date_converter, guage_decider
import mysql.connector
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:root@kraken-mysql-container-1:3306/currencies")

button_style = {
    "background-color": colors["--ls-increasing-color"],
    "color": colors["--ls-background-color"],
    "width": "50%",
}

def create_predict_button():
    return dbc.Button(
        id="trigger-predict-btn",
        children=["Predict"],
        className="btn-primary",
        style=button_style,
        n_clicks=0
    )

@callback(
    [
        Output(component_id='predict-btn', component_property='n_clicks'),
        Output(component_id='loading-container', component_property='style', allow_duplicate=True),
        Output(component_id='toast-container', component_property='children', allow_duplicate=True),
    ],
    Input(component_id='trigger-predict-btn', component_property='n_clicks'),
    [
        State(component_id='currencies-store', component_property='data'),
        State(component_id='method-store', component_property='data'),
        State(component_id='predict-days-store', component_property='data'),
    ],
    prevent_initial_call=True,
)
def trigger_click_predict_button(n_clicks: int, currencies_store: any, method_store: any, predict_days_store: any):
    if not all([currencies_store, method_store, predict_days_store]):
        return 0, {'display': 'none'}, create_toast(msg="Fill in all the fields", is_success=False)
    return 1, {'display': 'block'}, None


@callback(
    [
        Output(component_id='graph', component_property='figure'),
        Output(component_id={'type': 'guage', 'index': 'RSI'}, component_property='value'),
        Output(component_id={'type': 'guage', 'index': 'SMA'}, component_property='value'),
        Output(component_id={'type': 'guage', 'index': 'WMA'}, component_property='value'),
        Output(component_id={'type': 'guage', 'index': 'EMA'}, component_property='value'),
    ],
    Input(component_id='predict-btn', component_property='n_clicks'),
    [
        State(component_id='currencies-store', component_property='data'),
        State(component_id='method-store', component_property='data'),
        State(component_id='predict-days-store', component_property='data'),
        State(component_id={'type': 'dropdown', 'index': 'RSI'}, component_property='value'),
        State(component_id={'type': 'dropdown', 'index': 'SMA'}, component_property='value'),
        State(component_id={'type': 'dropdown', 'index': 'WMA'}, component_property='value'),
        State(component_id={'type': 'dropdown', 'index': 'EMA'}, component_property='value'),
    ],
    prevent_initial_call=True,
)
def click_predict_button(n_clicks: int, currencies_store: any, method_store: any, predict_days_store: any, rsi_days: str, sma_days: str, wma_days: str, ema_days: str):
    if not all([currencies_store, method_store, predict_days_store]):
        raise PreventUpdate

    query = "SELECT * FROM eur_pln"
    df = pd.read_sql_query(query, engine)

    forecast = forecaster.get_forecast(df=df, days=predict_days_store, time_step=7)
    next_days = list(np.reshape(forecast, (forecast.shape[0])))

    start_day = df.tail(1)["Date"].values[0] + timedelta(days=1)
    first_date = df.tail(1)["Date"].values[0]
    mapped_days = []
    i = 0
    while i < len(next_days):
        if start_day.weekday() >= 5:
            start_day += timedelta(days=1)
        else:
            mapped_days.append(date_converter.date2str(start_day))
            start_day += timedelta(days=1)
            i += 1

    avail_data = 365
    show_data = 30 + predict_days_store

    df_part = df[['Date', 'Close']][-avail_data:]
    result_df = pd.concat([df_part, pd.DataFrame({"Date": mapped_days, "Close": next_days})], ignore_index=True)


    figure = create_graph(df=result_df, graph_type="line", currencies=currencies_store)
    figure.update_layout(
        shapes = [dict(x0=first_date, x1=first_date, y0=0, y1=1, xref='x', yref='paper', line_width=4, line=dict(color=colors["--ls-decreasing-color"]))],
        annotations=[dict(x=first_date, y=0.05, xref='x', yref='paper', showarrow=False, xanchor='left', text='Predicted')],
        xaxis_range=[result_df["Date"].tail(show_data).values[0], result_df["Date"].tail(1).values[0]],
        yaxis_range=[result_df["Close"].tail(show_data).min(), result_df["Close"].tail(show_data).max()],
    )
    
    
    decision_0 = guage_decider.get_decision_RSI(result_df, days=int(rsi_days.split(' ')[0]))
    decision_1 = guage_decider.get_decision_MA(result_df, MA_type="SMA", days=int(sma_days.split(' ')[0]))
    decision_2 = guage_decider.get_decision_MA(result_df, MA_type="WMA", days=int(wma_days.split(' ')[0]))
    decision_3 = guage_decider.get_decision_MA(result_df, MA_type="EMA", days=int(ema_days.split(' ')[0]))

    return figure, decision_0, decision_1, decision_2, decision_3


@callback(
    [
        Output(component_id='loading-container', component_property='style', allow_duplicate=True),
        Output(component_id='toast-container', component_property='children', allow_duplicate=True),
    ],
    Input(component_id='graph', component_property='figure'),
    prevent_initial_call=True,
)
def calc_finished(graph):
    if not graph:
        raise PreventUpdate
    return {'display': 'none'}, create_toast(msg="Calculations were completed", is_success=True)
