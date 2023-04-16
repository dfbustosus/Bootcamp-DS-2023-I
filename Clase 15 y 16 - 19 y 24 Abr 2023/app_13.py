import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import json

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
token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'
with open('us.json') as f:
    geojson = json.loads(f.read())

def category_month_scatter_plot(df, states=None, start_date=None, end_date=None):
    data = []
    
    subcategory_grouped = df.groupby(['Category'], as_index=False)
    for name, group in subcategory_grouped:
        grouped = group.groupby('YearMonth', as_index=False).sum()
        data.append(go.Scatter(
            x=grouped['YearMonth'], y=grouped['Sales'], name=name
        ))
    
    return data

def category_bar_plot(df, states=None, start_date=None, end_date=None):
    data = []
    category_grouped = df.groupby(['Category'], as_index=False).sum()
    data.append(go.Bar(
        x=category_grouped['Category'], y=category_grouped['Sales'], name='Sales'
    ))
    data.append(go.Bar(
        x=category_grouped['Category'], y=category_grouped['Profit'], name='Profit'
    ))
    return data

df = pd.read_csv('superstore.csv', parse_dates=['Order Date'])
df['YearMonth'] = pd.to_datetime(df['Order Date'].map(lambda x: "{}-{}".format(x.year, x.month)))
df['State_abbr'] = df['State'].map(us_state_abbrev)
states_grouped = df.groupby(['State_abbr'], as_index=False).sum()
states_grouped['Sales_State'] = states_grouped[['State_abbr', 'Sales']].apply(lambda x: 'Sales for {}: {:.2f}$'.format(x[0], x[1]), axis=1)

df['YearMonth'] = pd.to_datetime(df['Order Date'].map(lambda x: "{}-{}".format(x.year, x.month)))

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/uditagarwal/pen/oNvwKNP.css'])

app.layout = html.Div(children=[
    html.Div(
        children=[
            html.H2(children="US Sales Dashboard", className='h2-title'),
            html.Div(
                className='div-logo padding-top-bot',
                children=[
                    dcc.DatePickerRange(
                    id='date-picker-range', # The id of the DatePicker, its always very important to set an Id for all our components
                    start_date=df['Order Date'].min(), # The start_date is going to be the min of Order Date in our dataset
                    end_date=df['Order Date'].max(),
                )
                ]
            )
        ],
        className='study-browser-banner row'
    ),
    html.Div(
        className='row app-body', 
        children=[
            html.Div(
                className='twelve columns card-left',
                children=[
                    html.Div(
                        dcc.Graph(
                            id='map-plot',
                            figure={ 
                                'data': [go.Choroplethmapbox(
                                    geojson=geojson,
                                    locations=states_grouped['State_abbr'],
                                    z=states_grouped['Sales'],
                                    colorscale='Viridis',
                                    text=states_grouped['Sales_State'],
                                    colorbar_title="Thousands USD"
                                )],
                                'layout': go.Layout(
                                        mapbox_style="dark",
                                        mapbox_accesstoken=token,
                                        mapbox_zoom=3,
                                        margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},
                                        mapbox_center={"lat": 37.0902, "lon": -95.7129}
                                    )
                            }
                        ),
                    ),
                ]),
            html.Div( # New Div
                className='twelve columns',
                children=[
                    html.Div(
                        className='six columns',
                        children=[dcc.Graph(
                            id='category-scatter-plot', # Plot 1
                            figure={
                                'data': category_month_scatter_plot(df),
                                'layout': go.Layout(
                                    margin={'t': 10, 'r': 10,}
                                )
                            },
                        )]
                    ),
                    html.Div(
                        className='six columns',
                        children=[dcc.Graph(id='category-bar-plot', figure={'data': category_bar_plot(df), 'layout':{'barmode': 'group'}})]
                    ),
                ]
            )]
        )]
)


@app.callback(
    dash.dependencies.Output('map-plot', 'figure'), # component with id map-plot will be changed, the 'figure' argument is updated
    [
        dash.dependencies.Input('date-picker-range', 'start_date'), # input with id date-picker-range and the start_date parameter
        dash.dependencies.Input('date-picker-range', 'end_date')
    ]
)
def update_sales_map(start_date, end_date):
    dff = df[(df['Order Date'] >= start_date) & (df['Order Date'] < end_date)] # We filter our dataset for the daterange
    states_grouped = dff.groupby(['State_abbr'], as_index=False).sum()  # We group our data again
    states_grouped['Sales_State'] = states_grouped[['State_abbr', 'Sales']].apply(lambda x: 'Sales for {}: {:.2f}$'.format(x[0], x[1]), axis=1)

    return { 
            'data': [go.Choroplethmapbox(
                geojson=geojson,
                locations=states_grouped['State_abbr'],
                z=states_grouped['Sales'],
                colorscale='Viridis',
                text=states_grouped['Sales_State'],
                colorbar_title="Thousands USD"
            )],
            'layout': go.Layout(
                    mapbox_style="dark",
                    mapbox_accesstoken=token,
                    mapbox_zoom=3,
                    margin={'t': 10, 'l': 10, 'r': 10, 'b': 10},
                    mapbox_center = {"lat": 37.0902, "lon": -95.7129}
                )
        }


@app.callback(
    dash.dependencies.Output('category-scatter-plot', 'figure'),
    [
        dash.dependencies.Input('map-plot', 'selectedData'),
        dash.dependencies.Input('date-picker-range', 'start_date'),
        dash.dependencies.Input('date-picker-range', 'end_date')
    ]
)
def update_scatter_plot(map_data, start_date, end_date):
    states = [each['location'] for each in map_data['points']] if map_data else None # extract states
    data = category_month_scatter_plot(df, states, start_date, end_date)
    return {
        'data': data,
        'layout': go.Layout(
            margin={'t': 10, 'r': 10,}
        )
    }


@app.callback(
    dash.dependencies.Output('category-bar-plot', 'figure'),
    [
        dash.dependencies.Input('map-plot', 'selectedData'),
        dash.dependencies.Input('date-picker-range', 'start_date'),
        dash.dependencies.Input('date-picker-range', 'end_date')
    ]
)
def update_bar_plot(map_data, start_date, end_date):

    states = [each['location'] for each in map_data['points']] if map_data else None # extract states
    data = category_bar_plot(df, states, start_date, end_date)

    return {
        'data': data,
        'layout': go.Layout(
            margin={'t': 10, 'r': 10,}
        )
    }


if __name__ == "__main__":
    app.run_server(debug=False)