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

df_unemployment_rate = pd.read_csv('unemployment_rate.csv')

df_claims = pd.read_csv('unemployment_claims.csv')

df_map = pd.read_csv('unemployment_rate.csv')
for col in df_map.columns:
    df_map[col] = df_map[col].astype(str)
df_map['text'] = df_map['State'] + ': ' + df_map['UEP Rate'] 

## dropdown
features = df_unemployment_rate.State.unique()
opts = [{'label' : i, 'value' : i} for i in features]
## Range Slider
un_dates = list(df_unemployment_rate.Month.unique())
## Slider
date_map = list(df_map.Month.unique())

################ Step 3. Create a plotly figure ################

df_unemployment_rate_0 = df_unemployment_rate[df_unemployment_rate['code']=='AL']
df_claims_0 = df_claims[df_claims['code']=='AL']

trace_1 = go.Scatter(x = df_unemployment_rate_0['Month'], y = df_unemployment_rate_0['UEP Rate'],
                    name = 'Alabama',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
layout1 = go.Layout(title = 'Time Series for Unemployment Rate',
                   hovermode = 'x',
                   spikedistance =  -1,
                   xaxis=dict(
                       #showline=True, 
                       #showgrid=True, 
                       showticklabels=True,
                       spikemode  = 'across+toaxis',
                       #linecolor='rgb(204, 204, 204)',
                       linewidth=0.5,
                       mirror=True)                       
                       )

trace_2 = go.Scatter(x = df_claims_0['date'], y = df_claims_0['claims'],
                    name = 'Alabama',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))

linetrace = go.Scatter(
                x=[df_claims_0['date'][357],df_claims_0['date'][357]], # , '2020-03-09', '2020-03-12','2020-03-27', '2020-03-27', '2020-04-19'],
                y=[0, -3], # -3, 71, 74, 71, 71],
                text=["1st death reported",
                    "in the US"],
                    # "First Trading Curb",
                    # 'Second Trading Curb',
                    # "Trump signs",
                    # "Stimulus bill",
                    # "U.S Oil Price Hits $15"],
                mode="text",
            )

linetrace2 = go.Scatter(x = [df_claims_0['date'][357], df_claims_0['date'][357]],
                         y = [0,140000],
                         mode = 'lines',
                         line = dict(color = "black",width=1, dash="dashdot")
                        )           


layout2 = go.Layout(title = 'Time Series for Emerging Unemployment Claims',
                   hovermode = 'x',
                   spikedistance =  -1,
                   xaxis=dict(
                       #showline=True, 
                       #showgrid=True, 
                       showticklabels=True,
                       spikemode  = 'across+toaxis',
                       #linecolor='rgb(204, 204, 204)',
                       linewidth=0.5,
                       mirror=True))

fig1 = go.Figure(data = [trace_1], layout = layout1)
fig2 = go.Figure(data = [trace_2, linetrace, linetrace2], layout = layout2)

################ Step 4. Create a Dash layout ################ 

app.layout = html.Div([
                # adding a header and a paragraph
                html.Div([
                    html.H1("This is my first dashboard"),
                    html.P("Learning Dash is so interesting!!")
                         ], 
                    style = {'padding' : '50px' , 
                             'backgroundColor' : '#d5d0f7'}),

                # adding a plot
                dcc.Graph(id='map'),        
                dcc.Graph(id = 'plot1'),# figure = fig1),
                dcc.Graph(id = 'plot2'), #figure = fig2),
                # dropdown
                html.P([
                    html.Label("Select any states"),
                    dcc.Dropdown(id = 'opt', 
                                 options = opts,
                                 placeholder="Select any states",
                                 value = [opts[0]['value'],  opts[2]['value']],                                 
                                 searchable=True,                              
                                 multi=True)
                        ], style = {'width': '400px',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'}),
                # range slider
                html.P([
                    html.Label("Time Period"),
                    dcc.RangeSlider(id = 'RangeSlider_wm',
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
                                    value = [0, 62],
                                    allowCross=True
                                    )           
                        ],  style = {
                                    'width' : '87%',
                                    'fontSize' : '20px',
                                    'padding-left' : '60px',
                                    'padding-right' : '100px',
                                    'display': 'inline-block'
                                    }),
                # # slider
                # html.P([
                #     html.Label("Time"),
                #     dcc.Slider(id = 'slider',
                #                     marks = {0:{'label':'Jan 2015'}, 1:{'label':''}, 2:{'label':''}, 3:{'label':''}, 
                #                     4:{'label':''}, 5:{'label':''}, 6:{'label':'July 2015'}, 7:{'label':''}, 
                #                     8:{'label':''}, 9:{'label':''}, 10:{'label':''}, 11:{'label':''}, 
                #                     12:{'label':'Jan 2016'}, 13:{'label':''}, 14:{'label':''}, 15:{'label':''}, 
                #                     16:{'label':''}, 17:{'label':''}, 18:{'label':'July 2016'}, 19:{'label':''}, 
                #                     20:{'label':''}, 21:{'label':''}, 22:{'label':''}, 23:{'label':''}, 
                #                     24:{'label':'Jan 2017'}, 25:{'label':''}, 26:{'label':''}, 27:{'label':''}, 
                #                     28:{'label':''}, 29:{'label':''}, 30:{'label':'July 2017'}, 31:{'label':''}, 
                #                     32:{'label':''}, 33:{'label':''}, 34:{'label':''}, 35:{'label':''}, 
                #                     36:{'label':'Jan 2018'}, 37:{'label':''}, 38:{'label':''}, 39:{'label':''}, 
                #                     40:{'label':''}, 41:{'label':''}, 42:{'label':'July 2018'}, 43:{'label':''}, 
                #                     44:{'label':''}, 45:{'label':''}, 46:{'label':''}, 47:{'label':''},
                #                     48:{'label':'Jan 2019'}, 49:{'label':''}, 50:{'label':''}, 51:{'label':''}, 
                #                     52:{'label':''}, 53:{'label':''}, 54:{'label':'July 2019'}, 55:{'label':''}, 
                #                     56:{'label':''}, 57:{'label':''}, 58:{'label':''}, 59:{'label':''}, 
                #                     60:{'label':'Jan 2020'}, 61:{'label':''}, 62:{'label':'Mar 2020'}},
                #                     min = 0,
                #                     max = 62,
                #                     value = 50,
                #                     included = False                                    
                #                     )
                                    
                        # ],  style = {
                        #             'width' : '87%',
                        #             'fontSize' : '20px',
                        #             'padding-left' : '60px',
                        #             'padding-right' : '100px',
                        #             'display': 'inline-block'
                        #             })
                      ])
                   
################ Step 5. Add callback functions ################ 
@app.callback([Output('map', 'figure'),Output('plot1', 'figure'),Output('plot2', 'figure')],
             [Input('opt', 'value'),Input('RangeSlider_wm','value'),])


def update_figure(un_state,un_time):
    
    # filtering the data
    df_unemployment_rate_2 = df_unemployment_rate[(df_unemployment_rate.Month >= un_dates[un_time[0]]) & (df_unemployment_rate.Month <= un_dates[un_time[1]])]
    df_new_un = df_map[df_map['Month']== date_map[un_time[0]]]

    traces_1 = []
    traces_2 = []
 
    highesty = 0
    for val in un_state:
        df_unemployment_rate_1 = df_unemployment_rate_2[(df_unemployment_rate_2.State == val)]
        df_claims_1 = df_claims[df_claims['State'] == val]

        traces_1.append(go.Scatter(
            x = df_unemployment_rate_1['Month'],
            y = df_unemployment_rate_1['UEP Rate'],
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

        if df_claims_1['claims'].max() > highesty:
            highesty = df_claims_1['claims'].max()
    
    linetrace = go.Scatter(
                x=[df_claims_0['date'][357], df_claims_0['date'][459],  df_claims_0['date'][561]],
                y=[highesty+2000, highesty+2000, highesty+2000],
                text=["1st death reported in the US",
                    "Week of Trading Curbs",
                    "Trump signs Stimulus bill"
                    ],
                    # "Trump signs",
                    # "Stimulus bill",
                    # "U.S Oil Price Hits $15"],
                mode="text",
            )
    linetrace2 = go.Scatter(x = [df_claims_0['date'][357], df_claims_0['date'][357]],
                            y = [0,highesty],
                            mode = 'lines',
                            line = dict(color = "black",width=1, dash="dashdot")
                            )  
    linetrace3 = go.Scatter(x = [df_claims_0['date'][459], df_claims_0['date'][459]],
                            y = [0,highesty],
                            mode = 'lines',
                            line = dict(color = "black",width=1, dash="dashdot")
                            )   
    linetrace4 = go.Scatter(x = [df_claims_0['date'][561], df_claims_0['date'][561]],
                            y = [0,highesty],
                            mode = 'lines',
                            line = dict(color = "black",width=1, dash="dashdot")
                            )   

    traces_2.append(linetrace)
    traces_2.append(linetrace2)   
    traces_2.append(linetrace3)  
    traces_2.append(linetrace4)  

    fig1 = go.Figure(data = traces_1, layout = layout1)

    fig2 = go.Figure(data = traces_2, layout = layout2)

    fig3 = go.Figure(data=go.Choropleth(
            locations=df_new_un['code'],
            z=df_new_un['UEP Rate'].astype(float),
            colorscale='Reds',
            locationmode = 'USA-states',
            text=df_new_un['text'], # hover text
            colorbar_title = "Percent",
        ))

    fig3.update_layout(
            title_text = 'Unemployment Rate by State',
            geo_scope='usa') # limite map scope to USA)
    
    return fig1, fig2, fig3

################ Step 6. Add the server clause ################ 

if __name__ == '__main__':
    app.run_server(debug = True,port=8022)

