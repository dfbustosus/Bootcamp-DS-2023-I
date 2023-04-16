import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go


app = dash.Dash(__name__)

df = pd.read_csv('superstore.csv', parse_dates=['Order Date', 'Ship Date'])
df = df[(df['Order Date'] > '2015-01-01') & (df['Order Date'] < '2016-01-01')]
df['month'] = pd.DatetimeIndex(df['Order Date']).month
dff = df.groupby('month', as_index=False).sum()
dff['Total Sales'] = dff['Sales'].cumsum()

app.layout = dcc.Graph(
        id='Data Plot',
        figure={
            'data': [
                go.Scatter(name='Sales', x=dff['month'], y=dff['Sales']),
                go.Scatter(name='Profit', x=dff['month'], y=dff['Profit']),
                go.Scatter(name='Total Sales', x=dff['month'], y=dff['Total Sales'])
            ],
            'layout': {
                'title': 'Sales & Profit in 2015',
                'xaxis': {'title': 'Month'}
            }
        }
    )


if __name__ == "__main__":
    app.run_server(debug=False)