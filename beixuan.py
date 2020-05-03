import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Step 1. Launch the application
app = dash.Dash()
# Step 2. Import the dataset
df_google = pd.read_csv('US_Corona.csv')
df_apple = pd.read_csv('apple_mobility.csv')
# category dropdown 
# state and county dropdown
state = df_google['State'].unique()
Dict = {}
for s in state:
    df_1 = df_google[df_google['State'] == s]
    df_2 = df_1[['State', 'County']]
    Dict[s] = df_2['County'].unique()

opt_state = options=[{'label': k, 'value': k} for k in Dict.keys()]
# date slide bar
df_google['Date'] = pd.to_datetime(df_google.Date)
df_apple['Date'] = pd.to_datetime(df_apple.Date)
dates = ['2020-02-29', '2020-03-07', '2020-03-14', '2020-03-21',
         '2020-03-28', '2020-04-04', '2020-04-11']

# Step 3. Create a plotly figure
##############################################################################
### Google Mobility
fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=("Retail", "Grocery", "Parks", 
                    "Transit", "Work", "Residential"))

df0 = df_google[(df_google['State'] == "The Whole Country")]

fig.add_trace(go.Scatter(x = df0.Date, y = df0.Retail,
                    name = 'Retail',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)')),
                    row=1, col=1)

fig.add_trace(go.Scatter(x = df0.Date, y = df0.Grocery,
                    name = 'Grocery',
                    line = dict(width = 2,
                                color = 'rgb(51, 218, 230)')),
                    row=1, col=2)

fig.add_trace(go.Scatter(x = df0.Date, y = df0.Parks,
                    name = 'Parks',
                    line = dict(width = 2,
                                color = 'rgb(61, 202, 169)')),
                    row=1, col=3)

fig.add_trace(go.Scatter(x = df0.Date, y = df0.Transit,
                    name = 'Transit',
                    line = dict(width = 2,
                                color = 'rgb(148, 147, 159)')),
                    row=2, col=1)

fig.add_trace(go.Scatter(x = df0.Date, y = df0.Work,
                    name = 'Work',
                    line = dict(width = 2,
                                color = 'rgb(143, 132, 242)')),
                    row=2, col=2)

fig.add_trace(go.Scatter(x = df0.Date, y = df0.Residential,
                    name = 'Residential',
                    line = dict(width = 2,
                                color = 'rgb(242, 132, 227)')),
                    row=2, col=3)

fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10))

fig.update_layout(height=500, width=700, 
                    title = 'Time Series Plot for Mobility in' + str(df0['County'][0]),
                    hovermode = 'closest', 
                    shapes = [{'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':'2020-03-07', 'x1':'2020-04-04', 
                               'xref':'x1','yref':'y1',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                              {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':'2020-03-07', 'x1':'2020-04-04',
                               'xref':'x2','yref':'y2',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                              {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':'2020-03-07', 'x1':'2020-04-04',
                                       'xref':'x3','yref':'y3',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':'2020-03-07', 'x1':'2020-04-04',
                                       'xref':'x4','yref':'y4',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':'2020-03-07', 'x1':'2020-04-04',
                                       'xref':'x5','yref':'y5',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':'2020-03-07', 'x1':'2020-04-04',
                                       'xref':'x6','yref':'y6',
                               'line': {'color': 'black', 'width': 0.5}
                               }
                      ])

##############################################################################
### Apple Mobility
# Define cities
city = ['New York City', 'Rome', 'London', 'Berlin', 'Toronto', 'Tokyo']
fig_app = make_subplots(
    rows=2, cols=3,
    subplot_titles=('New York City', 'Rome', 'London', 'Berlin', 'Toronto', 'Tokyo'))

df_US = df_apple[(df_apple['Region'] == city[0])]
####### NYC
traceapp1 = go.Scatter(x = df_US.Date, y = df_US.driving,
                    name = 'Driving',
                    mode='lines',
                    line = dict(width = 1,
                                color = 'rgb(131, 90, 241)'),
                    stackgroup='one')
                                

traceapp2 = go.Scatter(x = df_US.Date, y = df_US.transit,
                    name = 'Transit',
                    mode='lines',
                    line = dict(width = 1,
                                color = 'rgb(111, 231, 219)'),
                    stackgroup='one')

traceapp3 = go.Scatter(x = df_US.Date, y = df_US.walking,
                    name = 'Walking',
                    mode='lines',
                    line=dict(width = 1, 
                              color='rgb(102, 255, 102)'),
                    stackgroup='one')

fig_app.add_trace(traceapp3,
              row=1, col=1)
fig_app.add_trace(traceapp2,
              row=1, col=1)
fig_app.add_trace(traceapp1,
              row=1, col=1)

for c in range(1, len(city)): 
#    print(c, city[c])
    df_apple_city = df_apple[(df_apple['Region'] == city[c])]
    
    traceapp1 = go.Scatter(x = df_apple_city.Date, y = df_apple_city.driving,
                    name = 'Driving',
                    mode='lines',
                    line = dict(width = 1,
                                color = 'rgb(131, 90, 241)'),
                    stackgroup='one', showlegend= False)
                                

    traceapp2 = go.Scatter(x = df_apple_city.Date, y = df_apple_city.transit,
                        name = 'Transit',
                        mode='lines',
                        line = dict(width = 1,
                                    color = 'rgb(111, 231, 219)'),
                        stackgroup='one', showlegend= False)
    
    traceapp3 = go.Scatter(x = df_apple_city.Date, y = df_apple_city.walking,
                        name = 'Walking',
                        mode='lines',
                        line=dict(width = 1, 
                                  color='rgb(102, 255, 102)'),
                        stackgroup='one', showlegend= False)
    if(c < 3): 
        fig_app.add_trace(traceapp3,
              row=1, col=c+1)
        fig_app.add_trace(traceapp2,
                      row=1, col=c+1)
        fig_app.add_trace(traceapp1,
                      row=1, col=c+1)
    
    else: 
        fig_app.add_trace(traceapp3,
              row=2, col=c-2)
        fig_app.add_trace(traceapp2,
                      row=2, col=c-2)
        fig_app.add_trace(traceapp1,
                      row=2, col=c-2)
        
fig_app.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10))

fig_app.update_layout(height=500, width=700, 
                    title = 'Time Series Plot for Mobility',
                    hovermode = 'x unified')
                 
# Step 4. Create a Dash layout
app.layout = html.Div([
                # adding a header and a paragraph
                html.Div([
                    html.H1("US Mobility Data"),
                    html.P("Learning Dash is so interesting!!")
                         ], 
                    style = {'padding' : '50px' , 
                             'backgroundColor' : '#3aaab2'}),
                
                dcc.Graph(id = 'all_fig'),
                dcc.Graph(id = 'google_fig'),
                
                # range slider
                html.P([
                    html.Label("Time Period"),
                    dcc.RangeSlider(id = 'slider',
                                    marks = {i : dates[i] for i in range(0, 7)},
                                    min = 0,
                                    max = 6,
                                    value = [1, 5])
                        ], style = {'width' : '85%',
                                    'fontSize' : '18px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'}),

                
                 html.P([
                    html.Label("Choose a state"),
                    dcc.Dropdown(id = 'opt_s', options = opt_state,
                                value = 'The Whole Country')
                        ], style = {'width': '400px',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'}),
    
                html.P([
                    html.Label("Choose a county"),
                    dcc.Dropdown(id = 'opt_c')
                        ], style = {'width': '400px',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'})

])



## Step 5. Add callback functions
@app.callback(
    Output('opt_c', 'options'),
    [Input('opt_s', 'value')])
def set_state_options(selected_state):
    return [{'label': i, 'value': i} for i in Dict[selected_state]]

@app.callback(
    Output('opt_c', 'value'),
    [Input('opt_c', 'options')])
def set_county_value(available_options):
    return available_options[0]['value']

@app.callback(Output('google_fig', 'figure'),
              [Input('slider', 'value'), 
               Input('opt_s', 'value'), Input('opt_c', 'value')])

def update_figure(input2, selected_state, selected_county):
    df_3 = df_google[(df_google['State'] == selected_state) & (df_google['County'] == selected_county)]
    df_3 = df_3.sort_values(['Date']).reset_index(drop=True)
    df_4 = df_3[(df_3['Date'] >= dates[input2[0]]) & (df_3['Date'] < dates[input2[1]])]
    df_4 = df_4.sort_values(['Date']).reset_index(drop=True)
    
###############################################################################
#### Google Mobility
    fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=("Retail", "Grocery", "Parks", 
                    "Transit", "Work", "Residential"))
    
    fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Retail,
                        name = 'Retail',
                        fill = 'tozeroy',
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)')),
                        row=1, col=1)
    
    fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Grocery,
                        name = 'Grocery',
                        fill = 'tozeroy',
                        line = dict(width = 2,
                                    color = 'rgb(51, 218, 230)')),
                        row=1, col=2)
    
    fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Parks,
                        name = 'Parks',
                        fill = 'tozeroy',
                        line = dict(width = 2,
                                    color = 'rgb(61, 202, 169)')),
                        row=1, col=3)
    
    fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Transit,
                        name = 'Transit',
                        fill = 'tozeroy',
                        line = dict(width = 2,
                                    color = 'rgb(148, 147, 159)')),
                        row=2, col=1)
    
    fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Work,
                        name = 'Work',
                        fill = 'tozeroy',
                        line = dict(width = 2,
                                    color = 'rgb(143, 132, 242)')),
                        row=2, col=2)
    
    fig.add_trace(go.Scatter(x = df_4.Date, y = df_4.Residential,
                        name = 'Residential',
                        fill = 'tozeroy',
                        line = dict(width = 2,
                                    color = 'rgb(242, 132, 227)')),
                        row=2, col=3)
    
    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10))
    
    if (df_3['State'][0] == "The Whole Country"):
        fig.update_layout(height=500, width=700, 
                    title = 'Time Series Plot for Mobility in ' + str(df_4['County'][0]),
                    hovermode = 'closest')
        
        fig['layout'].update(shapes = [{'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x1', 'yref':'y1',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x2', 'yref':'y2',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x3','yref':'y3',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x4','yref':'y4',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x5','yref':'y5',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x6','yref':'y6',
                               'line': {'color': 'black', 'width': 0.5}
                               }
                              ])
                
    else: 
        fig.update_layout(height=500, width=700, 
                        title = 'Time Series Plot for Mobility in ' + str(df_4['County'][0]) + ', ' + str(df_3['State'][0]),
                        hovermode = 'closest')
        
        fig['layout'].update(shapes = [{'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x1','yref':'y1',
                               'line': {'color': 'black', 'width': 0.5}
                               }, 
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x2','yref':'y2',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x3','yref':'y3',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x4','yref':'y4',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x5','yref':'y5',
                               'line': {'color': 'black', 'width': 0.5}
                               },
                               {'type': 'line', 'y0':0, 'y1': 0, 
                                       'x0':min(df_4.Date), 'x1':max(df_4.Date),
                                       'xref':'x6','yref':'y6',
                               'line': {'color': 'black', 'width': 0.5}
                               }                          
                              ])
    
    
    return fig

##############################################################################
### Apple Mobility
@app.callback(Output('all_fig', 'figure'), 
              [Input('slider', 'value')])

def update_fig(input2):
#    df_apple_US = df_apple[(df_apple['Region'] == "Tokyo")]
    fig_app = make_subplots(
    rows=2, cols=3,
    subplot_titles=('New York City', 'Rome', 'London', 'Berlin', 'Toronto', 'Tokyo'))
    
    df_US = df_apple[(df_apple['Region'] == city[0])]
    df_apple_US = df_US[(df_US['Date'] >= dates[input2[0]]) & (df_US['Date'] < dates[input2[1]])]
    
    traceapp1 = go.Scatter(x = df_apple_US.Date, y = df_apple_US.driving,
                        name = 'Driving',
                        mode='lines',
                        line = dict(width = 1,
                                    color = 'rgb(131, 90, 241)'),
                        stackgroup='one')
                                    
    
    traceapp2 = go.Scatter(x = df_apple_US.Date, y = df_apple_US.transit,
                        name = 'Transit',
                        mode='lines',
                        line = dict(width = 1,
                                    color = 'rgb(111, 231, 219)'),
                        stackgroup='one')
    
    traceapp3 = go.Scatter(x = df_apple_US.Date, y = df_apple_US.walking,
                        name = 'Walking',
                        mode='lines',
                        line=dict(width = 1, 
                                  color='rgb(102, 255, 102)'),
                        stackgroup='one')
    
    fig_app.add_trace(traceapp3,
              row=1, col=1)
    fig_app.add_trace(traceapp2,
                  row=1, col=1)
    fig_app.add_trace(traceapp1,
                  row=1, col=1)

    for c in range(1, len(city)): 
    #    print(c, city[c])
        df_apple_city = df_apple[(df_apple['Region'] == city[c])]
        df_apple_new = df_apple_city[(df_apple_city['Date'] >= dates[input2[0]]) & (df_apple_city['Date'] < dates[input2[1]])]
        
        traceapp1 = go.Scatter(x = df_apple_new.Date, y = df_apple_new.driving,
                        name = 'Driving',
                        mode='lines',
                        line = dict(width = 1,
                                    color = 'rgb(131, 90, 241)'),
                        stackgroup='one', showlegend= False)
                                    
    
        traceapp2 = go.Scatter(x = df_apple_new.Date, y = df_apple_new.transit,
                            name = 'Transit',
                            mode='lines',
                            line = dict(width = 1,
                                        color = 'rgb(111, 231, 219)'),
                            stackgroup='one', showlegend= False)
        
        traceapp3 = go.Scatter(x = df_apple_new.Date, y = df_apple_new.walking,
                            name = 'Walking',
                            mode='lines',
                            line=dict(width = 1, 
                                      color='rgb(102, 255, 102)'),
                            stackgroup='one', showlegend= False)
        if(c < 3): 
            fig_app.add_trace(traceapp3,
                  row=1, col=c+1)
            fig_app.add_trace(traceapp2,
                          row=1, col=c+1)
            fig_app.add_trace(traceapp1,
                          row=1, col=c+1)
        
        else: 
            fig_app.add_trace(traceapp3,
                  row=2, col=c-2)
            fig_app.add_trace(traceapp2,
                          row=2, col=c-2)
            fig_app.add_trace(traceapp1,
                          row=2, col=c-2)
            
    fig_app.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10))
    
    fig_app.update_layout(height=500, width=700, 
                        title = 'Time Series Plot for Mobility',
                        hovermode = 'x unified')

    return fig_app

if __name__ == "__main__":
    app.run_server(debug=True, port=3004, use_reloader=False)
