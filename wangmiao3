# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)
server = app.server

df_lockdown = pd.read_csv('lockdown_new.csv')
df_lockdown = df_lockdown[(df_lockdown['code']!= 'DC') ]
df_lockdown['order'] = df_lockdown['type'].map({0: 'No lockdown order', 0.5: 'Partial lockdown', 
                                                1:'Statewide lockdown',0.75:'Essential business reopen',
                                                0.55: 'Partial reopen'})
for col in df_lockdown.columns: 
    df_lockdown[col] = df_lockdown[col].astype(str)

df_lockdown['text'] = df_lockdown['date'] +'\n' + df_lockdown['state'] + ': ' + df_lockdown['order'] 
lockdown_date = list(df_lockdown.date.unique())

color1 = [ "#ead6ee", "#aebaf8"]
color2 = ["#e8f5c8","#aebaf8"]

app.layout = html.Div([  
                dcc.Graph(id='map_lockdown'),
                # Add a slider
                html.P([
                    html.Label("Time"),
                    dcc.Slider(id = 'lockdown_slider',
                                    marks = {0:{'label':'3/19/20'}, 6:{'label':'3/25/20'},
                                    12:{'label':'3/31/20'}, 19:{'label':'4/7','style': {'color': '#f50'}},
                                    20:{'label':'4/21','style': {'color': '#f50'}},
                                    27:{'label':'4/30/20'}, 31:{'label':'5/4/20'} 
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
                                    }),
                html.Div([
                    #html.H1("This is my first dashboard"),
                    html.P("Notes: "),
                    html.P("1) Until Apr 7, 42 states have implemented stay-at-home orders."),
                    html.P("2) Started from Apr 21, governers have taken different stategies to reopen their states."),
                    html.P("Data Source: CNN, The New York Times, CNBC")
                         ],
                     style = {'padding' : '50px' }
                    )
                ])

@app.callback(Output('map_lockdown', 'figure'),
            [Input('lockdown_slider', 'value')])

def update_figure(time_lockdown):

    lockdown_new = df_lockdown[df_lockdown['date'] == lockdown_date[time_lockdown]]

    if time_lockdown <= 19:
        fig = go.Figure(data=go.Choropleth(
                locations=lockdown_new['code'],
                z=lockdown_new['type'],
                autocolorscale = False,
                colorscale= color1,            
                locationmode = 'USA-states',
                
                text= lockdown_new['text'],  # hover text
                colorbar={'dtick':0.5,
                        'tickmode':'array',
                        'ticktext':['No lockdown order','Partial lockdown','Statewide lockdown'],
                        'tickvals':[0,0.5,1]
                        }               
            ))
    else:
        fig = go.Figure(data=go.Choropleth(
                locations=lockdown_new['code'],
                z=lockdown_new['type'],
                autocolorscale = False,
                colorscale= color2,            
                locationmode = 'USA-states',
                text= lockdown_new['text'],  # hover text
                #colorbar_title = "Percent",
                
                colorbar={'dtick':0.25,
                        'tickmode':'array',
                        'ticktext':['Partial reopen','Essential business reopen','Statewide lockdown'],
                        'tickvals':[0.55,0.75,1]
                        }               
            ))
       
    fig.update_layout(
    title_text = 'Lockdown Timeline by States',
    geo_scope='usa',
    margin=dict(l=10, r=40, t=40, b=40)
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    