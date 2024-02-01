import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd
from utils.colors import colors

def create_candlestick_graph(df: pd.DataFrame, disabled: bool = False, name: str = None) -> go:
    return go.Candlestick(
        name=name,
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color=colors["--ls-increasing-color"] if not disabled else colors["--ls-increasing-disabled-color"],
        decreasing_line_color=colors["--ls-decreasing-color"] if not disabled else colors["--ls-decreasing-disabled-color"],
    )

def create_line_graph(df: pd.DataFrame, disabled: bool = False, name: str = None):
    return go.Scatter(
        name=name,
        x=df['Date'],
        y=df['Close'],
        line=dict(color=colors["--ls-increasing-color"] if not disabled else colors["--ls-increasing-disabled-color"]),
    )

def create_graph(df: pd.DataFrame, disabled: bool = False, graph_type: str = "candlestick", currencies=["EUR", "PLN"]) -> go.Figure:
    data = None
    new_df = df
    if graph_type == "candlestick":
        data = create_candlestick_graph(df=new_df, disabled=disabled, name="-".join(currencies))
    else:
        data = create_line_graph(df=new_df, disabled=disabled, name="-".join(currencies))

    return go.Figure(
        data=[data],
        layout={
            "plot_bgcolor": colors["--ls-transparent-color"],
            "paper_bgcolor": colors["--ls-transparent-color"],
            "font": {"color": colors["--ls-text-color"]},
            "yaxis": {"gridcolor": colors["--ls-grid-color"]},
            "xaxis": {"gridcolor": colors["--ls-grid-color"]},
            "legend": {
                "bordercolor": colors["--ls-increasing-color"] if not disabled else colors["--ls-increasing-disabled-color"],
                "borderwidth": 1,
                "yanchor": "bottom",
                "y": 1,
                "xanchor":"left",
                "x": 0
            },
            "showlegend": True,
            "margin": {"t": 30, "l": 5, "b": 5, "r": 5}
        }
    )
