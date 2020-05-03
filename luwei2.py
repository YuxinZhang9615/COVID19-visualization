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

app = dash.Dash()
server = app.server


daterange = pd.date_range(start='3/22/2020',end='4/29/2020',freq='D')
daterange = [str(pd.to_datetime(x, unit='s').date()) for x in daterange]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

markdict = {0: {'label': '2020-03-22'},
            1: {'label': ''}, 2: {'label': ''}, 3: {'label': ''}, 4: {'label': ''},
            5: {'label': '2020-03-27'}, 
            6: {'label': ''}, 7: {'label': ''}, 8: {'label': ''}, 9: {'label': ''},
            10: {'label': '2020-04-01'},
            11: {'label': ''}, 12: {'label': ''}, 13: {'label': ''}, 14: {'label': ''},
            15: {'label': '2020-04-06'},
            16: {'label': ''}, 17: {'label': ''}, 18: {'label': ''}, 19: {'label': ''},
            20: {'label': '2020-04-11'},
            21: {'label': ''}, 22: {'label': ''}, 23: {'label': ''}, 24: {'label': ''},
            25: {'label': '2020-04-16'}, 
            26: {'label': ''}, 27: {'label': ''}, 28: {'label': ''}, 29: {'label': ''},
            30: {'label': '2020-04-21'},
            31: {'label': ''}, 32: {'label': ''}, 33: {'label': ''}, 
            34: {'label': '2020-04-25'},
            35: {'label': ''}, 36: {'label': ''}, 37: {'label': ''},
            38: {'label': '2020-04-29'}}


app.layout = html.Div([
    html.H1('Twitter Hot Words', id='time-range-label'),
    #html.Section(id="slideshow", children=[
        #html.Div(id="slideshow-container", children=[
        dcc.Slider(
            id='year-slider',
            updatemode = 'mouseup',
            min=0,
            max=38,
            value=38,
            marks=markdict,
            step=1),
        #html.Div(id="slide-container"),
        html.Div(id="image"),
        dcc.Graph(id ='hot-table', style={'display': 'inline-block'})
        #], style={'width': '100%', 'display': 'inline-block'})
    #])
])

#print({x: {'label' : str(pd.to_datetime(x, unit='s').date())} for x in daterange['date'].unique()})



@app.callback(
    dash.dependencies.Output('image', 'children'),
    [Input('year-slider', 'value')])


def update_output(value):
    src1 = "https://raw.githubusercontent.com/yyyyyokoko/covid-19-challenge/master/twitterViz/images/" + daterange[value] + '.png'
    img = html.Img(src=src1,  style={'height':'50%', 'width':'50%', 'display': 'inline-block'})
    return img
    # if value:
    #     print(pd.to_datetime(value, unit='s'))
    #     return pd.to_datetime(value, unit='s')

# @app.callback(
#     dash.dependencies.Output('slide-container', 'children'),
#     [Input('year-slider', 'value')])

# def slider_output(value):
#     return "Twitter Hot Words"

@app.callback(
    dash.dependencies.Output('hot-table', 'figure'),
    [Input('year-slider', 'value')])

def table_output(value):
    filename = "https://raw.githubusercontent.com/yyyyyokoko/covid-19-challenge/master/twitterViz/newcsv/" + daterange[value] + '.csv'
    df = pd.read_csv(filename)
    #temp = temp.iloc[1:-1,:].reset_index(drop = True)
    #df['rank'] = df.index + 1

    if daterange[value] != "2020-03-22":
        #red : New , yello: 上涨， green: 下降
        font_color=['black']
        temp = []
        df['change'] = pd.to_numeric(df['change'], errors='coerce')
        for i in df['change']:
            if np.isnan(i):
                temp.append('rgb(248, 112, 96)')
            else:
                if i >= 0:
                    temp.append('rgb(246, 189, 96)')
                else:
                    temp.append('rgb(132, 236, 157)')
        font_color.append(temp)
        print(font_color)
        data=[go.Table(
            columnwidth = [80,40,40],
            header=dict(values=['Keywords', 'Hottness'],
                        line_color= 'gainsboro',
                        fill_color='rgb(16, 37, 66)',
                        font=dict(color='rgb(238, 240, 242)'),
                        align='left'),
            cells=dict(values=[df['word'], df['count']],
                    line_color= 'gainsboro',
                    fill=dict(color=['rgb(247, 237, 226)', 'white']),
                    font_color=font_color,
                    align= ['left']*3))]
    else:
        data=[go.Table(
            columnwidth = [80,40,40],
            header=dict(values=list(df.columns),
                        line_color= 'gainsboro',
                        fill_color='rgb(16, 37, 66)',
                        font=dict(color='rgb(238, 240, 242)'),
                        align='left'),
            cells=dict(values=[df['word'], df['count']],
                    line_color= 'gainsboro',
                    fill=dict(color=['rgb(247, 237, 226)', 'white']),
                    align='left'))]

    return dict(data = data)



if __name__ == '__main__':
    app.run_server(debug=True)