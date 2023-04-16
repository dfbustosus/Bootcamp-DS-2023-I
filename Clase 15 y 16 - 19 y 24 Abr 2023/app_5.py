import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go


app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/uditagarwal/pen/oNvwKNP.css'])

app.layout = html.Div(children=[
    html.Div(
        children=[html.H2(children="US Sales Dashboard", className='h2-title'),],
        className='study-browser-banner row'
    )
])

if __name__ == "__main__":
    app.run_server(debug=False)