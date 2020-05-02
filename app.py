import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import random
import re
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Output, Input

import math

########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='Beer Comparison'
tabtitle='beer!'
myheading='Flying Dog Beers'
label1='IBU'
label2='ABV'
githublink='https://github.com/austinlasseter/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'


#################################################################
##############################      Table 3      ################
legal = pd.read_csv('covid-19-legislation.csv')
legal.drop('Internal Quorum Link', axis = 1, inplace = True)
legal.rename(columns= {'Status Text': 'Status'}, inplace = True)
legal = legal[legal['Region'] != "Puerto Rico"].reset_index(drop = True)
legal.replace(np.nan, '', inplace = True)

legal['search_area'] = legal[['COVID-19 Legislation', 'Official Description']].agg('.'.join, axis=1)
legal['search_area'] = legal['search_area'].str.lower()
legal['search_area'] = [re.sub('[^A-Za-z0-9]+', ' ', str(x)) for x in legal['search_area']]
legal['search_area'] = [re.sub(' ', '', str(x)) for x in legal['search_area']]

legal['link'] = ['<a href="'] * len(legal['Source Link']) + legal['Source Link'] + ['">click here</a>']
legal['title'] = ['<a href="'] * len(legal['Source Link']) + legal['Source Link'] + ['">'] + legal['COVID-19 Legislation'] + ['</a>']
legal['c'] = np.full(legal.shape[0], 1)
legal['code'] = [x.split(':')[0] for x in legal['COVID-19 Legislation']]


########### Set up the chart
bitterness = go.Bar(
    x=legal['Region'],
    y=legal['c'],
    name=label1,
    marker={'color':color1}
)
alcohol = go.Bar(
    x=beers,
    y=abv_values,
    name=label2,
    marker={'color':color2}
)

beer_data = [bitterness, alcohol]
beer_layout = go.Layout(
    barmode='group',
    title = mytitle
)

beer_fig = go.Figure(data=beer_data, layout=beer_layout)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(
                        dbc.NavbarBrand("COVID-19 Visualization", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

LEGAL_TABLE = [
    dbc.CardHeader(html.H5("Legislation Search Table")),
    dbc.CardBody([

        dbc.Row([
            dbc.Col([
                html.Label("Search By Keywords", style = {'fontSize': 15}),
                dcc.Input(id = "search_text",
                            type = 'search',
                            placeholder="Example: covid19, unemployment",
                            debounce = True,
                            style={'width': 330, 'height': 36})

                ], width = 4),

            dbc.Col([
                html.Label("Search By States", style = {'fontSize': 15}),
                dcc.Dropdown(
                    id = 'selected_state',
                    options = [{'label': x, 'value': x} for x in legal['Region'].unique()])
                ], width = 4),
            dbc.Col([
                html.Label("Search By Status", style = {'fontSize': 15}),
                dcc.Dropdown(
                    id = 'selected_status',
                    options = [{'label': x, 'value': x} for x in legal['Status'].unique()])
                ], width = 4)

            ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id = "legal_table")
                ], width = 6),
            dbc.Col([
                dcc.Graph(
                    figure = px.bar(legal, x="c", y="Region", color='Status', orientation='h', text = 'code',
                         height=580, 
                         color_discrete_sequence=["#DB5461", "#FAC9B8","#749BC1","#98A6D4",'#F4E409','#A6D3A0'],
                        ).update_traces(hovertemplate= '<b>%{text}</b>')
                         .update_layout(xaxis_showgrid=False, yaxis_showgrid=False, legend_orientation="h",
                                        font=dict(size=8),
                                        legend=dict(x=-.1, y=1.09),
                                        margin=dict(l=0, r=0, t=50, b=0, pad=0),
                                        plot_bgcolor='#f5f7fa')
                         .update_xaxes(title_text='').update_yaxes(title_text=''),
                    )

                ], width = 6, style = {'borderLeft': 'thin darkgrey solid', 'padding': '2px 15px 0px 0px',
                                       'margin': '10px 0px 0px 0px'})
            
            ])
            
        ])

]

BODY = dbc.Container(
    [
        #dbc.Row([dbc.Col(dbc.Card(FLATTEN_THE_CURVE)),], style={"marginTop": 30}),
        #dbc.Row([dbc.Col(dbc.Card(SURVEY_MEDIA)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col([dbc.Card(LEGAL_TABLE)])], style={"marginTop": 50})
    ],
    className="mt-12",
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[NAVBAR, BODY])

##### Legal Table 
@app.callback(Output("legal_table", "figure"),
    [Input("search_text", "value"),
     Input("selected_state", "value"),
     Input("selected_status", "value")])

def update_table(search_text, selected_state, selected_status):
    df = legal

    if search_text != None:
        keywords = re.split(',', search_text)
        keywords = [x.lower() for x in keywords]
        keywords = [re.sub('[^A-Za-z0-9]+', ' ', str(x)) for x in keywords]
        keywords = [re.sub(' ', '', str(x)) for x in keywords]

        for keyword in keywords:
            df = df[df['search_area'].str.contains(keyword)==True]

    if selected_state != None:
        df = df[(df['Region'] == selected_state)] 
    if selected_status != None:
        df = df[(df['Status'] == selected_status)]

    data = [go.Table(
                columnwidth = [400,200,200,200,150],
                header=dict(values=['<b>COVID-19 Legislation</b>', '<b>State</b>',
                                    '<b>Status</b>', '<b>Last Timeline Action</b>', '<b>Last Action Date</b>'],
                            fill_color='#91ADC2',
                            #fill_color='#87BBA2',
                            #fill_color='#4D5382',
                            font_color='white',
                            align='left'),
                cells=dict(values=[df['title'], df['Region'],
                                   df['Status'], df['Last Timeline Action'], df['Last Timeline Action Date']
                                   ],
                           fill_color='#f5f7fa',
                           align=['left','left','left','left','center']))
            ]
    layout = dict(height = 580,
                  margin=dict(t=25, b=20, l=0, r=10, pad=0))

    return dict(data = data, layout = layout)


if __name__ == '__main__':
    app.run_server()