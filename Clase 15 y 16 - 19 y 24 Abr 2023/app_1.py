import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

app = dash.Dash(__name__)
colors = ['red', 'green', 'blue', 'black']
df = pd.read_csv('superstore.csv', parse_dates=['Order Date', 'Ship Date'])
region_grouped = df.groupby(['Region'], as_index=False).sum()

app.layout = html.Div(children=[
    html.H1(children="Profit by Region", style={"textAlign": "center"}),
    dcc.Graph(
            id='regional-profit-plot',
            figure={
                'data': [
                    go.Bar(
                        name='Regional Profit',
                        marker_color=colors,
                        x=region_grouped['Region'],
                        y=region_grouped['Profit']
                    )],
            }
        )
])

app.run_server(debug=False)