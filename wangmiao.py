# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go


################ Step 1. Launch the application ################

app = dash.Dash()

################ Step 2. Import the dataset ################

df = pd.read_csv('unemployment_rate.csv')
df_claims = pd.read_csv('unemployment_claims.csv')
df_map = df
for col in df_map.columns:
    df_map[col] = df_map[col].astype(str)
df_map['text'] = df_map['State'] + ': ' + df_map['UEP Rate'] 

## dropdown
features = df.State.unique()
opts = [{'label' : i, 'value' : i} for i in features]
## range slider
dates = list(df.Month.unique())
## slider
date_map = list(df_map.Month.unique())

################ Step 3. Create a plotly figure ################

# df0 = df[df['code']=='AL']
# df_claims_0 = df_claims[df_claims['code']=='AL']

# trace_1 = go.Scatter(x = df0['Month'], y = df0['UEP Rate'],
#                     name = 'Alabama',
#                     line = dict(width = 2,
#                                 color = 'rgb(229, 151, 50)'))
layout1 = go.Layout(title = 'Time Series for Unemployment Rate',
                   hovermode = 'x',
                   spikedistance =  -1,
                   xaxis=dict(
                       showticklabels=True,
                       spikemode  = 'across+toaxis',
                       linewidth=0.5,
                       mirror=True)                       
                       )

# trace_2 = go.Scatter(x = df_claims_0['date'], y = df_claims_0['claims'],
#                     name = 'Alabama',
#                     line = dict(width = 2,
#                                 color = 'rgb(229, 151, 50)'))
layout2 = go.Layout(title = 'Time Series for the Emerging Unemployment Claims',
                   hovermode = 'x',
                   spikedistance =  -1,
                   xaxis=dict(
                       showticklabels=True,
                       spikemode  = 'across+toaxis',
                       linewidth=0.5,
                       mirror=True))

# fig1 = go.Figure(data = [trace_1], layout = layout1)
# fig2 = go.Figure(data = [trace_2], layout = layout2)

################ Step 4. Create a Dash layout ################ 

app.layout = html.Div([
                # adding 3 plots
                dcc.Graph(id='map'),        
                dcc.Graph(id = 'plot1'),# figure = fig1),
                dcc.Graph(id = 'plot2'), #figure = fig2),
                # dropdown - select states - plot 1 & plot 2
                html.P([
                    html.Label("Select any states"),
                    dcc.Dropdown(id = 'opt', 
                                 options = opts,
                                 placeholder="Select any states",
                                 value = opts[0]['value'],                                 
                                 searchable=True,                              
                                 multi=True)
                        ], style = {'width': '400px',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'}),
                # range slider - select time period - plot 2
                html.P([
                    html.Label("Time Period"),
                    dcc.RangeSlider(id = 'RangeSlider',
                                    marks = {0:{'label':'Jan 2015'}, 1:{'label':''}, 2:{'label':''}, 3:{'label':''}, 
                                    4:{'label':''}, 5:{'label':''}, 6:{'label':'July 2015'}, 7:{'label':''}, 
                                    8:{'label':''}, 9:{'label':''}, 10:{'label':''}, 11:{'label':''}, 
                                    12:{'label':'Jan 2016'}, 13:{'label':''}, 14:{'label':''}, 15:{'label':''}, 
                                    16:{'label':''}, 17:{'label':''}, 18:{'label':'July 2016'}, 19:{'label':''}, 
                                    20:{'label':''}, 21:{'label':''}, 22:{'label':''}, 23:{'label':''}, 
                                    24:{'label':'Jan 2017'}, 25:{'label':''}, 26:{'label':''}, 27:{'label':''}, 
                                    28:{'label':''}, 29:{'label':''}, 30:{'label':'July 2017'}, 31:{'label':''}, 
                                    32:{'label':''}, 33:{'label':''}, 34:{'label':''}, 35:{'label':''}, 
                                    36:{'label':'Jan 2018'}, 37:{'label':''}, 38:{'label':''}, 39:{'label':''}, 
                                    40:{'label':''}, 41:{'label':''}, 42:{'label':'July 2018'}, 43:{'label':''}, 
                                    44:{'label':''}, 45:{'label':''}, 46:{'label':''}, 47:{'label':''},
                                    48:{'label':'Jan 2019'}, 49:{'label':''}, 50:{'label':''}, 51:{'label':''}, 
                                    52:{'label':''}, 53:{'label':''}, 54:{'label':'July 2019'}, 55:{'label':''}, 
                                    56:{'label':''}, 57:{'label':''}, 58:{'label':''}, 59:{'label':''}, 
                                    60:{'label':'Jan 2020'}, 61:{'label':''}, 62:{'label':'Mar 2020'}},
                                    min = 0,
                                    max = 62,
                                    value = [0, 62]
                                    )           
                        ],  style = {
                                    'width' : '87%',
                                    'fontSize' : '20px',
                                    'padding-left' : '60px',
                                    'padding-right' : '100px',
                                    'display': 'inline-block'
                                    }),
                # slider - select date for map
                html.P([
                    html.Label("Time"),
                    dcc.Slider(id = 'slider',
                                    marks = {0:{'label':'Jan 2015'}, 1:{'label':''}, 2:{'label':''}, 3:{'label':''}, 
                                    4:{'label':''}, 5:{'label':''}, 6:{'label':'July 2015'}, 7:{'label':''}, 
                                    8:{'label':''}, 9:{'label':''}, 10:{'label':''}, 11:{'label':''}, 
                                    12:{'label':'Jan 2016'}, 13:{'label':''}, 14:{'label':''}, 15:{'label':''}, 
                                    16:{'label':''}, 17:{'label':''}, 18:{'label':'July 2016'}, 19:{'label':''}, 
                                    20:{'label':''}, 21:{'label':''}, 22:{'label':''}, 23:{'label':''}, 
                                    24:{'label':'Jan 2017'}, 25:{'label':''}, 26:{'label':''}, 27:{'label':''}, 
                                    28:{'label':''}, 29:{'label':''}, 30:{'label':'July 2017'}, 31:{'label':''}, 
                                    32:{'label':''}, 33:{'label':''}, 34:{'label':''}, 35:{'label':''}, 
                                    36:{'label':'Jan 2018'}, 37:{'label':''}, 38:{'label':''}, 39:{'label':''}, 
                                    40:{'label':''}, 41:{'label':''}, 42:{'label':'July 2018'}, 43:{'label':''}, 
                                    44:{'label':''}, 45:{'label':''}, 46:{'label':''}, 47:{'label':''},
                                    48:{'label':'Jan 2019'}, 49:{'label':''}, 50:{'label':''}, 51:{'label':''}, 
                                    52:{'label':''}, 53:{'label':''}, 54:{'label':'July 2019'}, 55:{'label':''}, 
                                    56:{'label':''}, 57:{'label':''}, 58:{'label':''}, 59:{'label':''}, 
                                    60:{'label':'Jan 2020'}, 61:{'label':''}, 62:{'label':'Mar 2020'}},
                                    min = 0,
                                    max = 62,
                                    value = 50,
                                    included = False                                    
                                    )                                  
                        ],  style = {
                                    'width' : '87%',
                                    'fontSize' : '20px',
                                    'padding-left' : '60px',
                                    'padding-right' : '100px',
                                    'display': 'inline-block'
                                    })
                      ])
                   
################ Step 5. Add callback functions ################ 

@app.callback([Output('plot1', 'figure'),Output('plot2', 'figure'),Output('map', 'figure')],
             [Input('opt', 'value'),Input('RangeSlider','value'),Input('slider', 'value')])

def update_figure(state1,time1,time_map):
    # filtering the data
    df2 = df[(df.Month >= dates[time1[0]]) & (df.Month <= dates[time1[1]])]
    df_new = df_map[df_map['Month']== date_map[time_map]]

    traces_1 = []
    traces_2 = []

    for val in state1:
        df1 = df2[(df2.State == val)]
        df_claims_1 = df_claims[df_claims['State'] == val]

        traces_1.append(go.Scatter(
            x = df1['Month'],
            y = df1['UEP Rate'],
            text= val,
            name = val,
            mode = 'lines',
            showlegend=True,           
        ))

        traces_2.append(go.Scatter(
            x = df_claims_1['date'],
            y = df_claims_1['claims'],
            text= val,
            name = val,
            mode = 'lines',
            showlegend=False
        ))
    
    fig1 = go.Figure(data = traces_1, layout = layout1)

    fig2 = go.Figure(data = traces_2, layout = layout2)

    fig3 = go.Figure(data=go.Choropleth(
            locations=df_new['code'],
            z=df_new['UEP Rate'].astype(float),
            colorscale='Reds',
            locationmode = 'USA-states',
            text=df_new['text'], # hover text
            colorbar_title = "Percent"))    
    fig3.update_layout(
            title_text = 'Unemployment Rate by State',
            geo_scope='usa') # limite map scope to USA)
    
    return fig1, fig2, fig3

################ Step 6. Add the server clause ################ 

if __name__ == '__main__':
    app.run_server(debug = True)
