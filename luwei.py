import dash
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import datetime as dt
import time
import pandas as pd
import base64
import flask
import glob
import os

import dash_bootstrap_components as dbc

app = dash.Dash()
server = app.server


daterange = pd.DataFrame(pd.date_range(start='3/22/2020',end='4/22/2020',freq='D'), columns = ['date'])
daterange['date'] = [x.timestamp() for x in daterange['date']]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



# TWEETER = [
#     dbc.CardHeader(html.H5('Tweeter HoT Words ')),
#     dbc.CardBody([
#         dbc.Row([
#             dbc.Col([
#                 html.Label('WordCloud', id='time-range-label'),
#                 html.Div(id="image"),
#                 ], width = 6),

#             dbc.Col([
#                 dcc.Graph(id ='hot-table', style={'display': 'inline-block'})
#                 ], width = 6)
#             ]),
#         dbc.Row([
#             dcc.Slider(
#             id='year-slider',
#             updatemode = 'mouseup',
#             min=daterange['date'].min(),
#             max=daterange['date'].max(),
#             value=daterange['date'].min(),
#             marks={x: {'label' : str(pd.to_datetime(x, unit='s').date())} for x in daterange['date'].unique()},
#             step=86400)
#             ])
#         ])

# ]
# app.layout = html.Div(children=[TWEETER])

app.layout = html.Div([
    html.Label('WordCloud', id='time-range-label'),

        
        dcc.Slider(
            id='year-slider',
            updatemode = 'mouseup',
            min=daterange['date'].min(),
            max=daterange['date'].max(),
            value=daterange['date'].min(),
            marks={x: {'label' : str(pd.to_datetime(x, unit='s').date())} for x in daterange['date'].unique()},
            step=86400),
        html.Div(id="slide-container"),
        html.Div(id="image"),
        dcc.Graph(id ='hot-table', style={'display': 'inline-block'})
        

])

#print({x: {'label' : str(pd.to_datetime(x, unit='s').date())} for x in daterange['date'].unique()})



@app.callback(
    dash.dependencies.Output('image', 'children'),
    [Input('year-slider', 'value')])


def update_output(value):
    src1 = "https://raw.githubusercontent.com/yyyyyokoko/covid-19-challenge/master/twitterViz/images/" + str(pd.to_datetime(value, unit='s').date()) + '.png'
    img = html.Img(src=src1,  style={'height':'50%', 'width':'50%', 'display': 'inline-block'})
    return img
    # if value:
    #     print(pd.to_datetime(value, unit='s'))
    #     return pd.to_datetime(value, unit='s')

@app.callback(
    dash.dependencies.Output('slide-container', 'children'),
    [Input('year-slider', 'value')])

def slider_output(value):
    return str(pd.to_datetime(value, unit='s').date())

@app.callback(
    dash.dependencies.Output('hot-table', 'figure'),
    [Input('year-slider', 'value')])

def table_output(value):
    filename = "https://raw.githubusercontent.com/yyyyyokoko/covid-19-challenge/master/twitterViz/newcsv/" + str(pd.to_datetime(value, unit='s').date()) + '.csv'
    df = pd.read_csv(filename)
    #temp = temp.iloc[1:-1,:].reset_index(drop = True)
    #df['rank'] = df.index + 1
    
    if str(pd.to_datetime(value, unit='s').date()) != "2020-03-22":
        font_color=['black']*2+[['red' if boolv else 'black' for boolv in df['change'].str.contains('New')]]
        print(font_color)
        data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df['word'], df['count'], list(df['change'])],
                    line_color='darkslategray',
                    fill=dict(color=['lavender', 'white', 'white']),
                    #font_color=font_color,
                    align= ['left']*3))]
    else:
        data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df['word'], df['count']],
                    line_color='darkslategray',
                    fill=dict(color=['lavender', 'white']),
                    align='left'))]

    return dict(data = data)



if __name__ == '__main__':
    app.run_server(debug=True)