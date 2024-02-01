from dash import dcc, html, register_page, Input, Output, callback, clientside_callback, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from utils.colors import colors


def create_toast(msg: str = "", is_success: bool = True):
    return dbc.Toast(
        msg,
        id="toast",
        header="Success" if is_success else "Error",
        is_open=True,
        dismissable=True,
        duration=3000,
        icon="success" if is_success else "danger",
        style=success_style if is_success else error_style,
        header_style=header_style,
    )


success_style = {
    "position": "fixed",
    "top": 10,
    "right": 10,
    "width": 350,
    "height": 100,
    "backgroundColor": colors["--ls-grid-color"],
    "border": f"3px solid {colors['--ls-increasing-color']}",
    "color": "white",
}
error_style = {
    "position": "fixed",
    "top": 10,
    "right": 10,
    "width": 350,
    "height": 100,
    "backgroundColor": colors["--ls-grid-color"],
    "border": f"3px solid {colors['--ls-decreasing-color']}",
    "color": "white",
}
header_style = {
    "backgroundColor": colors["--ls-grid-color"],
    "color": "white",
}