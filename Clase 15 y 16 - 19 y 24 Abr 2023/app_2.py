import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

app.layout = html.Div(children=[ # an html Div
    html.H1(children='Regional Sales Dashboard'), # the first element of the div is an H1, the property children renders the text on the page
    html.P(children="Rendered and Developed using Dash", id="p-tag", style={'color': 'blue'}) # the second element is a P tag
])

if __name__ == "__main__":
    app.run_server(debug=False)