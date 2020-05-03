import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Step 1. Launch the application
app = dash.Dash()
# Step 2. Import the dataset
df = pd.read_csv('US_Corona.csv')
df_apple = pd.read_csv('apple_mobility.csv')
# category dropdown 
# state and county dropdown
state = df['State'].unique()
Dict = {}
for s in state:
    df1 = df[df['State'] == s]
    df2 = df1[['State', 'County']]
    Dict[s] = df2['County'].unique()

opt_state = options=[{'label': k, 'value': k} for k in Dict.keys()]
# date slide bar
df['Date'] = pd.to_datetime(df.Date)
df_apple['Date'] = pd.to_datetime(df_apple.Date)
dates = ['2020-02-29', '2020-03-07', '2020-03-14', '2020-03-21',
         '2020-03-28', '2020-04-04', '2020-04-11']

# Step 3. Create a plotly figure
##############################################################################
### Google Mobility
df0 = df[(df['State'] == "The Whole Country")]

trace1 = go.Scatter(x = df0.Date, y = df0.Retail,
                    name = 'Retail',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))

trace2 = go.Scatter(x = df0.Date, y = df0.Grocery,
                    name = 'Grocery',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))

trace3 = go.Scatter(x = df0.Date, y = df0.Parks,
                    name = 'Parks',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))

trace4 = go.Scatter(x = df0.Date, y = df0.Transit,
                    name = 'Transit',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))

trace5 = go.Scatter(x = df0.Date, y = df0.Work,
                    name = 'Work',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))

trace6 = go.Scatter(x = df0.Date, y = df0.Residential,
                    name = 'Residential',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))

layout1 = go.Layout(title = 'Time Series Plot for Retail Mobility',
                   hovermode = 'closest')

layout2 = go.Layout(title = 'Time Series Plot for Grocery Mobility',
                   hovermode = 'closest')

layout3 = go.Layout(title = 'Time Series Plot for Parks Mobility',
                   hovermode = 'closest')

layout4 = go.Layout(title = 'Time Series Plot for Transit Mobility',
                   hovermode = 'closest')

layout5 = go.Layout(title = 'Time Series Plot for Work Mobility',
                   hovermode = 'closest')

layout6 = go.Layout(title = 'Time Series Plot for Residential Mobility',
                   hovermode = 'closest')

fig1 = go.Figure(data = trace1, layout = layout1)
fig2 = go.Figure(data = trace2, layout = layout2)
fig3 = go.Figure(data = trace3, layout = layout3)
fig4 = go.Figure(data = trace4, layout = layout4)
fig5 = go.Figure(data = trace5, layout = layout5)
fig6 = go.Figure(data = trace6, layout = layout6)
##############################################################################
### Apple Mobility
df_apple_1 = df_apple[(df_apple['Region'] == "United States")]

traceapp1 = go.Scatter(x = df_apple_1.Date, y = df_apple_1.driving,
                    name = 'Driving',
                    mode='lines',
                    line = dict(width = 1,
                                color = 'rgb(131, 90, 241)'),
                    stackgroup='one')
                                

traceapp2 = go.Scatter(x = df_apple_1.Date, y = df_apple_1.transit,
                    name = 'Transit',
                    mode='lines',
                    line = dict(width = 1,
                                color = 'rgb(111, 231, 219)'),
                    stackgroup='one')

traceapp3 = go.Scatter(x = df_apple_1.Date, y = df_apple_1.walking,
                    name = 'Walking',
                    mode='lines',
                    line=dict(width = 1, 
                              color='rgb(102, 255, 102)'),
                    stackgroup='one')

all_layout = go.Layout(title = 'Time Series Plot for Apple Mobility',
                   hovermode = 'x unified')

all_trace = [traceapp1, traceapp2, traceapp3] 
all_figure = go.Figure(data = all_trace, layout = all_layout)
                 
# Step 4. Create a Dash layout
app.layout = html.Div([
                # adding a header and a paragraph
                html.Div([
                    html.H1("This is my first dashboard"),
                    html.P("Learning Dash is so interesting!!")
                         ], 
                    style = {'padding' : '50px' , 
                             'backgroundColor' : '#3aaab2'}),
                
                dcc.Graph(id = 'all_fig'),
                dcc.Graph(id = 'plot1'),
                dcc.Graph(id = 'plot2'),
                dcc.Graph(id = 'plot3'),
                dcc.Graph(id = 'plot4'),
                dcc.Graph(id = 'plot5'),
                dcc.Graph(id = 'plot6'),    

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

@app.callback([Output('plot1', 'figure'), Output('plot2', 'figure'), 
               Output('plot3', 'figure'), Output('plot4', 'figure'),
               Output('plot5', 'figure'), Output('plot6', 'figure')],
              [Input('slider', 'value'), 
               Input('opt_s', 'value'), Input('opt_c', 'value')])

def update_figure(input2, selected_state, selected_county):
    df3 = df[(df['State'] == selected_state) & (df['County'] == selected_county)]
    df4 = df3[(df3['Date'] >= dates[input2[0]]) & (df3['Date'] < dates[input2[1]])]
    
##############################################################################
### Google Mobility
    data1 = [go.Scatter(x = df4.Date, y = df4.Retail,
                    fill = 'tozeroy',
                    name = 'Retail',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))]
                    
    data2 = [go.Scatter(x = df4.Date, y = df4.Grocery,
                fill = 'tozeroy',
                name = 'Grocery',
                line = dict(width = 2,
                            color = 'rgb(229, 151, 50)'))]
    
    data3 = [go.Scatter(x = df4.Date, y = df4.Parks,
                fill = 'tozeroy',
                name = 'Parks',
                line = dict(width = 2,
                            color = 'rgb(229, 151, 50)'))]
                    
    data4 = [go.Scatter(x = df4.Date, y = df4.Transit,
                fill = 'tozeroy',
                name = 'Work',
                line = dict(width = 2,
                            color = 'rgb(229, 151, 50)'))]
    
    data5 = [go.Scatter(x = df4.Date, y = df4.Work,
                fill = 'tozeroy',
                name = 'Transit',
                line = dict(width = 2,
                            color = 'rgb(229, 151, 50)'))]
    
    data6 = [go.Scatter(x = df4.Date, y = df4.Residential,
                fill = 'tozeroy',
                name = 'Residential',
                line = dict(width = 2,
                            color = 'rgb(229, 151, 50)'))]
                    


    fig1 = go.Figure(data = data1, layout = layout1)
    fig2 = go.Figure(data = data2, layout = layout2)
    fig3 = go.Figure(data = data3, layout = layout3)
    fig4 = go.Figure(data = data4, layout = layout4)
    fig5 = go.Figure(data = data5, layout = layout5)
    fig6 = go.Figure(data = data6, layout = layout6)
    
    
    return fig1, fig2, fig3, fig4, fig5, fig6

##############################################################################
### Apple Mobility
@app.callback(Output('all_fig', 'figure'), 
              [Input('slider', 'value')])

def update_fig(input2):
    df_apple1 = df_apple[(df_apple['Region'] == "United States")]
    df_apple2 = df_apple1[(df_apple1['Date'] >= dates[input2[0]]) & (df_apple1['Date'] < dates[input2[1]])]
    
    data_app1 = [go.Scatter(x = df_apple2.Date, y = df_apple2.driving,
#                    fill = 'tozeroy',
                    name = 'Driving',
                    mode='lines',
                    line=dict(width=1, color='rgb(131, 90, 241)'),
                    stackgroup='one')]
    
    data_app2 = [go.Scatter(x = df_apple2.Date, y = df_apple2.transit,
#                    fill = 'tozeroy',
                    name = 'Transit',
                    mode='lines',
                    line=dict(width=1, color='rgb(111, 231, 219)'),
                    stackgroup='one')]
    
    data_app3 = [go.Scatter(x = df_apple2.Date, y = df_apple2.walking,
#                    fill = 'tozeroy',
                    name = 'Walking',
                    mode='lines',
                    line=dict(width=1, color='rgb(102, 255, 102)'),
                    stackgroup='one')]
    
    data_app = data_app1 + data_app2 + data_app3
    
    all_figure = go.Figure(data = data_app, layout = all_layout)
    
    return all_figure

if __name__ == "__main__":
    app.run_server(debug=True, port=3004, use_reloader=False)
