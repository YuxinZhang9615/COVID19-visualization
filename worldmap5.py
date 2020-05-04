# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import datetime

app = dash.Dash(__name__)
server = app.server

import plotly.express as px

df_world = pd.read_csv('countryLockdown_date.csv')

df_world['area'] = df_world['type'].map({0: 'Not lockdown', 0.5: 'Partial lockdown', 1: 'Full lockdown'})

for col in df_world.columns: 
    df_world[col] = df_world[col].astype(str)

df_world['text'] = df_world['date'] + df_world['region'] + ': ' + df_world['area'] 

world_date = list(df_world.date.unique())
world_date = sorted(world_date, key=lambda date: datetime.datetime.strptime(date, "%m/%d/%y"))

color_lock = [ 'rgb(204,230,255)', 'rgb(133,122,173)', 'rgb(105,10,61)']
#color_lock = [ "#cce6ff", "#857aad", "#690a3d"]

app.layout = html.Div([              
                dcc.Graph(id='world_lockdown_map'),
                # Add a slider
                html.P([
                    html.Label("Time"),
                    dcc.Slider(id = 'world_lockdown_slider',
                                    marks = {0:{'label':'Jan 23'}, 1:{'label':''}, 2:{'label':''}, 3:{'label':'Feb 25'}, 
                                    4:{'label':''}, 5:{'label':''}, 6:{'label':'Mar 5'}, 7:{'label':''}, 
                                    8:{'label':''}, 9:{'label':''}, 10:{'label':'Mar 10'}, 11:{'label':''}, 
                                    12:{'label':''}, 13:{'label':''}, 14:{'label':''}, 15:{'label':'Mar 15'}, 
                                    16:{'label':''}, 17:{'label':''}, 18:{'label':''}, 19:{'label':''}, 
                                    20:{'label':'Mar 20'}, 21:{'label':''}, 22:{'label':''}, 23:{'label':''}, 
                                    24:{'label':''}, 25:{'label':'Mar 25'}, 26:{'label':''}, 27:{'label':''}, 
                                    28:{'label':'Mar 28'}, 29:{'label':''}, 30:{'label':'Mar 30'}, 31:{'label':''}
                                    },
                                    min = 0,
                                    max = 31,
                                    value = 16,
                                    included = False,
                                    updatemode='drag'                                    
                                    )           
                        ],  style = {
                                    'width' : '87%',
                                    'fontSize' : '20px',
                                    'padding-left' : '60px',
                                    'padding-right' : '100px',
                                    'display': 'inline-block'
                                    })
                ])

@app.callback(Output('world_lockdown_map', 'figure'),
            [Input('world_lockdown_slider', 'value')])

def update_figure(world_time):

    lockdown_new = df_world[df_world['date'] == world_date[world_time]]

    fig = px.choropleth(lockdown_new, locations="iso_alpha",
                    color="type",
                    hover_name="region", # column to add to hover information
                    color_continuous_scale=color_lock
                    #text= lockdown_new['text']
                    )
    fig.update_geos(lataxis_showgrid=False, lonaxis_showgrid=False, 
                    projection_type="natural earth",showcountries=True)             
    fig.update_layout(
    title_text = 'Worldwide Lockdown by Regions',
    margin=dict(l=10, r=40, t=40, b=40),
    coloraxis_showscale = False
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    