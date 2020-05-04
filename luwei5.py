import pandas as pd
import os
import plotly.graph_objs as go
import plotly.express as px
from copy import deepcopy
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Step 1. Launch the application
app = dash.Dash()

# Step 2. Import the dataset
basepath2 = 'generalTerms/'
files2 = os.listdir(basepath2)
files2.sort()

plotnames = []
for i in files2:
    a = pd.read_csv(basepath2 + i, skiprows = 1)
    colname = a.columns[1]
    plotnames.append(colname.split(':')[0])

def getData(i):
    a = pd.read_csv(basepath2 + i, skiprows = 1)
    a[['Year','Month', 'Day']] = a.Week.str.split('-', expand=True)
    colname = a.columns[1]
    a.columns.values[1] = colname.split(':')[0]
    #colname2 = a.columns[0].split('-')[1:]
    #a.columns.values[0] = "-".join(colname2)
    a = a[(a['Year'] == '2019') | (a['Year'] == '2020')]
    a = a[(a['Month'] == '01') | (a['Month'] == '02') | (a['Month'] == '03') | (a['Month'] == '04')]
    #a['Week'] = pd.to_datetime(a.Week)
    a['Week'] = ["/".join(x.split('-')[1:]) for x in a['Week']]
    df1 = a[(a['Year'] == '2019')]
    df2 = a[(a['Year'] == '2020')]
    df1.loc[:,'Week'] = df2.Week.values
    return df1 , df2

# Step 3. Create a plotly fig_lwure
##############################################################################
### Google 

fig_lw = make_subplots(rows=3, cols=4, subplot_titles=plotnames)



df2019, df2020= getData(files2[0])
traceapp1 = go.Scatter(x = df2019['Week'], y = df2019.iloc[:,1],
                name = '2019',
                mode='lines',
                legendgroup='group1',
                line = dict(width = 1,
                            color = 'rgb(111, 231, 219)'),
                fill='tozeroy')

traceapp2 = go.Scatter(x = df2020['Week'], y = df2020.iloc[:,1],
                    name = '2020',
                    legendgroup='group1',
                    mode='lines',
                    line = dict(width = 1,
                                color = 'red'),
                    fill='tozeroy')

fig_lw.add_trace(traceapp2, row=1, col=1)
fig_lw.add_trace(traceapp1, row=1, col=1)
fig_lw.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10), row=1, col=1)
fig_lw.update_yaxes(range=[0, 100], row=1, col=1)

for i in range(1, len(files2)):
    #print(i, files2[i])
    df2019, df2020= getData(files2[i])
    traceapp1 = go.Scatter(x = df2019['Week'], y = df2019.iloc[:,1],
                    name = '2019',
                    mode='lines',
                    line = dict(width = 1,
                                color = 'rgb(111, 231, 219)'),
                    fill='tozeroy',
                    showlegend= False)

    traceapp2 = go.Scatter(x = df2020['Week'], y = df2020.iloc[:,1],
                        name = '2020',
                        mode='lines',
                        line = dict(width = 1,
                                    color = 'red'),
                        fill='tozeroy',
                        showlegend= False)

    if i <= 3:
        fig_lw.add_trace(traceapp2, row=1, col=i+1)
        fig_lw.add_trace(traceapp1, row=1, col=i+1)
        fig_lw.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10), row=1, col=i+1)
        fig_lw.update_yaxes(range=[0, 100], row=1, col=i+1)

    elif 4 <= i <= 7:
        fig_lw.add_trace(traceapp2, row=2, col=i-3)
        fig_lw.add_trace(traceapp1, row=2, col=i-3)
        fig_lw.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10), row=2, col=i-3)
        fig_lw.update_yaxes(range=[0, 100], row=2, col=i-3)

    elif 8 <= i <= 11:
        fig_lw.add_trace(traceapp2, row=3, col=i-7)
        fig_lw.add_trace(traceapp1, row=3, col=i-7)
        fig_lw.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=10), row=3, col=i-7)
        fig_lw.update_yaxes(range=[0, 100], row=3, col=i-7)

fig_lw.update_traces(mode="lines", hovertemplate=None)
fig_lw.update_layout(width=1400, height=800, hovermode = 'x unified', showlegend= True, title = "Changes of Google Search Interest",
    )

# Step 4. Create a Dash layout
app.layout = html.Div([
                # adding a header and a paragraph
                html.Div([
                    html.H1("This is my first dashboard"),
                    html.P("Learning Dash is so interesting!!")], style = {'padding' : '50px' , 'backgroundColor' : '#3aaab2'}),
                html.Div(id="slideshow-container", children=[
                    dcc.Graph(figure = fig_lw)], style = {'display': 'inline-block'})
])


if __name__ == "__main__":
    app.run_server(debug=True, port=3004)
