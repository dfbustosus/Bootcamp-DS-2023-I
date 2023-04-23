import dash
import json
import operator
import random

from functools import reduce

import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from sqlalchemy import create_engine
from plotly.subplots import make_subplots
from pandas.api.types import CategoricalDtype


# Connect to SQL Engine and select all data
engine = create_engine('sqlite:///crime.db')
df = pd.read_sql("SELECT * from crime", engine.connect(), parse_dates=('OCCURRED_ON_DATE',))


def get_filtered_rows(crime_type, start_date, end_date):
    crime_len = ','.join('?'*len(crime_type))
    sql_query = f'SELECT * from crime WHERE OCCURRED_ON_DATE BETWEEN ? and ? AND OFFENSE_CODE_GROUP in ({crime_len})'
    
    sql_params = [start_date, end_date]
    for each in crime_type:
        sql_params.append(each)

    return pd.read_sql(sql_query, engine.connect(), params=sql_params, parse_dates=('OCCURRED_ON_DATE',))
    
def locations_by_crimetype(crime_type, start_date, end_date):
    data = []
    df = get_filtered_rows(crime_type, start_date, end_date)
    for name, group in df.groupby('OFFENSE_CODE_GROUP'):
        color = "%06x" % random.randint(0, 0xFFFFFF)
        data.append(
            go.Scattermapbox(
                lat=group['Lat'],
                lon=group['Long'],
                mode='markers',
                marker={
                    'color': '#' + color,
                },
                text=group['OFFENSE_DESCRIPTION'],
                name=name
            )
        )
    return data

def crimes_by_year(crime_type, start_date, end_date):
    data = []
    df = get_filtered_rows(crime_type, start_date, end_date)

    df['YearMonth'] = pd.to_datetime(df['OCCURRED_ON_DATE'].map(lambda x: "{}-{}".format(x.year, x.month)))

    for name, group in df.groupby('OFFENSE_CODE_GROUP'):
        grouped = group.groupby('YearMonth', as_index=False).count()
        data.append(
            go.Scatter(x=grouped['YearMonth'], y=grouped['Lat'], name=name)
        )
    return data


def crimes_by_district(crime_type, start_date, end_date):
    data = []
    df = get_filtered_rows(crime_type, start_date, end_date)

    for name, group in df.groupby('OFFENSE_CODE_GROUP'):
        grouped = group.groupby('DISTRICT', as_index=False).count()
        data.append(
            go.Bar(y=grouped['DISTRICT'], x=grouped['Lat'].sort_values(), name=name, orientation='h')
        )
    return data



def crimes_week(crime_type, start_date, end_date):
    cats = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    fig = make_subplots(rows=1, cols=7, subplot_titles=cats)
    dff = get_filtered_rows(crime_type, start_date, end_date)
    
    cat_type = CategoricalDtype(categories=cats, ordered=True)
    dff['DAY_OF_WEEK'] = dff['DAY_OF_WEEK'].astype(cat_type)

    for crime_name, group in dff.groupby('OFFENSE_CODE_GROUP'):
        i=1
        for day_of_week, week_group in group.groupby('DAY_OF_WEEK'):
            hour_group = week_group.groupby('HOUR', as_index=False).count()
            fig.append_trace(
                go.Scatter(x=hour_group['HOUR'], y=hour_group['Lat'], name=crime_name),
                row=1, col=i
            )
            i += 1
    
    fig.update_layout(
        title="Hourly/Weekly Crime Trends",
    )
    return fig
    

# Get Token for Mapbox & Read GeoJSON
token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'
app = dash.Dash(__name__)


app.layout = html.Div(children=[
    html.Div(
            children=[
                html.H2(children="Boston Crime Analysis", className='h2-title'),
            ],
            className='study-browser-banner row'
    ),
    html.Div(
        className="row app-body",
        children=[
            # User Controls
            html.Div(
                className="twelve columns card",
                children=[
                    html.Div(
                        className="four columns card",
                        children=[
                            html.Div(
                                className="bg-white user-control",
                                children=[
                                    html.Div(
                                        className="padding-top-bot",
                                        children=[
                                            html.H6("Select Crime Type"),
                                            dcc.Dropdown(
                                                id="study-dropdown",
                                                multi=True,
                                                value=('Larceny',),
                                                options=[{'label': label.title(), 'value': label.title()} for label in df['OFFENSE_CODE_GROUP'].unique()]
                                            ),
                                            html.H6("Select a Date"),
                                            dcc.DatePickerRange(
                                                id="date-range",
                                                start_date=df['OCCURRED_ON_DATE'].min(),
                                                end_date=df['OCCURRED_ON_DATE'].max()
                                            ),
                                        ],
                                    ),
                                ],
                            )
                        ],
                    ),
                    html.Div(
                        className='eight columns card',
                        children=[
                            html.H1(children="Geographical Map of Crimes in Boston", style={'textAlign': 'center'}),
                            dcc.Graph(
                                id='map-plot',
                                figure={ 
                                    'data': [go.Scattermapbox()],
                                    'layout': go.Layout(
                                            mapbox_style="dark",
                                            mapbox_accesstoken=token,
                                            mapbox_zoom=10,
                                            margin={'t': 0, 'l': 0, 'r': 0, 'b': 30},
                                            mapbox_center={"lat": df['Lat'][0], "lon": df['Long'][0]}
                                        )
                                }
                            )
                        ]
                    )
                    ]
            ),
            html.Div(
                className='twelve columns card 2',
                children=[
                    html.Div(
                        className='six columns card',
                        children=[
                            dcc.Graph(
                            id='crime-total-graph',
                            figure={
                                'data': [go.Scatter()],
                            }
                        )],
                    ),
                    html.Div(
                        className='six columns card 2',
                        children=[
                            dcc.Graph(
                                id='crime-district-graph',
                                figure={
                                    'data': [go.Bar()],
                                }
                            )
                        ])
                        ]
                    )
                ]
            ),
            html.Div(
                className='twelve columns card 3',
                children=[
                    dcc.Graph(
                        id="crimes-weekly",
                        figure={
                            'data': [go.Scatter()]
                        }
                    )
                ]
            )
        ]
    )


@app.callback(
    dash.dependencies.Output('map-plot', 'figure'), # component with id map-plot will be changed, the 'figure' argument is updated
    [
        dash.dependencies.Input('date-range', 'start_date'), # input with id date-picker-range and the start_date parameter
        dash.dependencies.Input('date-range', 'end_date'),
        dash.dependencies.Input('study-dropdown', 'value'),
    ]
)
def update_crimes_map(start_date, end_date, value):
    return { 
            'data': locations_by_crimetype(value, start_date, end_date),
            'layout': go.Layout(
                mapbox_style="dark",
                mapbox_accesstoken=token,
                mapbox_zoom=10,
                margin={'t': 0, 'l': 0, 'r': 0, 'b': 30},
                mapbox_center={"lat": df['Lat'][0], "lon": df['Long'][0]}
            )
        }



@app.callback(
    dash.dependencies.Output('crime-total-graph', 'figure'),
    [
        dash.dependencies.Input('date-range', 'start_date'), # input with id date-picker-range and the start_date parameter
        dash.dependencies.Input('date-range', 'end_date'),
        dash.dependencies.Input('study-dropdown', 'value'),
    ]
)
def update_crimes_line_plot(start_date, end_date, value):
    return { 
        'data': crimes_by_year(value, start_date, end_date),
        'layout': {
            'title': {
                'text': 'Crime Occurence over Time'
            }
        }
    }


@app.callback(
    dash.dependencies.Output('crime-district-graph', 'figure'),
    [
        dash.dependencies.Input('date-range', 'start_date'), # input with id date-picker-range and the start_date parameter
        dash.dependencies.Input('date-range', 'end_date'),
        dash.dependencies.Input('study-dropdown', 'value'),
    ]
)
def update_crimes_bar_plot(start_date, end_date, value):
    return { 
        'data': crimes_by_district(value, start_date, end_date),
        'layout': {
            'title': {
                'text': 'Crime Occurence by District',

            }
        }
    }


@app.callback(
    dash.dependencies.Output('crimes-weekly', 'figure'),
    [
        dash.dependencies.Input('date-range', 'start_date'), # input with id date-picker-range and the start_date parameter
        dash.dependencies.Input('date-range', 'end_date'),
        dash.dependencies.Input('study-dropdown', 'value'),
    ]
)
def update_crimes_subplots(start_date, end_date, value):
    return crimes_week(value, start_date, end_date)

if __name__ == "__main__":
    app.run_server(debug=True)
