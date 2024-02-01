from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
from components.navbar import create_navbar

app = Dash(
    name=__name__,
    use_pages=True,
    pages_folder="pages",
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.4.2/mdb.min.css",
    ]
)
app.title = 'Kraken'
app._favicon = ("images/kraken_icon.png")
app.layout = html.Div(
    children=[
        create_navbar(),
        page_container
    ]
)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run_server(debug=True, host='0.0.0.0', port=8050)