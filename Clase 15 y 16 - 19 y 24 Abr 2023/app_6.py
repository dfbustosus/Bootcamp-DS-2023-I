import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json
token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'
with open('us.json') as f:
    geojson = json.loads(f.read())

us_state_abbrev = {'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA',
                   'Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC',
                   'Florida': 'FL','Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL',
                   'Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA',
                   'Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN',
                   'Mississippi': 'MS','Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV',
                   'New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY',
                   'North Carolina': 'NC','North Dakota': 'ND','Northern Mariana Islands': 'MP',
                   'Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Palau': 'PW','Pennsylvania': 'PA',
                   'Puerto Rico': 'PR','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD',
                   'Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virgin Islands': 'VI',
                   'Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI',
                   'Wyoming': 'WY',}
df = pd.read_csv('superstore.csv', parse_dates=['Order Date'])
df['State_abbr'] = df['State'].map(us_state_abbrev)
states_grouped = df.groupby(['State_abbr'], as_index=False).sum()
states_grouped.head()

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/uditagarwal/pen/oNvwKNP.css'])

app.layout = html.Div(children=[
    html.Div(
        children=[html.H2(children="US Sales Dashboard", className='h2-title'),],
        className='study-browser-banner row'
    ),
    html.Div(
        className='row app-body', 
        children=[
        dcc.Graph(
            id='map-plot',
            figure={ 
                'data': [go.Choroplethmapbox(
                    geojson=geojson,
                    locations=states_grouped['State_abbr'],
                    z=states_grouped['Sales'],
                    colorscale='Viridis',
                    colorbar_title="Thousands USD"
                )],
                'layout': go.Layout(
                        mapbox_style="dark",
                        mapbox_accesstoken=token,
                        mapbox_zoom=2,
                        mapbox_center = {"lat": 37.0902, "lon": -95.7129}
                    )
            }
        )
])])


if __name__ == "__main__":
    app.run_server(debug=False)