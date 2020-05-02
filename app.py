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



######################################################################################################################
######################################################################################################################
#######################################         1.  Data              ################################################
######################################################################################################################
######################################################################################################################

####################################################################################
#######################   Page 1 - Plot1.   Flatten the Curve      ################
####################################################################################
def calculate_growth_rate_WORLD(df):
    
    df = df.drop(['Province/State', 'Lat', 'Long'], axis = 1)

    df =  df.groupby(['Country/Region']).sum().reset_index()

    df = df.transpose().reset_index()
    df.columns = df.iloc[0,:]
    df.drop([0], axis = 0, inplace = True)
    df.reset_index(drop = True, inplace = True)
    df.rename(columns = {'Country/Region' : 'Date'}, inplace = True)
    df.Date = pd.to_datetime(df.Date)

    df.drop(list(df.columns[1:][df.iloc[:,1:].sum(axis = 0) == 0]), axis = 1, inplace=True) 
    df.drop(['Iceland', 'Kazakhstan', 'Slovakia'], axis = 1, inplace = True)
    df.columns = ["South Korea" if x == "Korea, South" else x for x in list(df.columns)]

    dfR = pd.DataFrame(np.empty_like(df))
    dfR.columns = df.columns
    dfR['Date'] = df['Date']


    for i in range(1, df.shape[1]):
        country = df.columns[i]
        j = np.where(df[country] > 0)[0][0]
        dfR[country] = np.concatenate((np.full(j+5,np.nan), 
                                                pow(np.array(df[country][j+5:]) / np.array(df[country][j:df.shape[0]-5]), 1/5) - 1),
                                                axis = 0)  
    for i in range(1, dfR.shape[1]):
        s = [j for j in range(dfR.shape[0]) if not math.isnan(dfR.iloc[j,i])][0]
        
        for j in range(s+1, dfR.shape[0]-1):
            dfR.iloc[j, i] = np.mean([dfR.iloc[j-1, i],
                                                  dfR.iloc[j, i],
                                                  dfR.iloc[j+1, i]])
    return(dfR)

def calculate_growth_rate_US(df):
    
    df = df.drop(['UID','iso2','iso3','code3','FIPS','Admin2','Country_Region', 'Lat', 'Long_','Combined_Key'], axis = 1)


    df =  df.groupby(['Province_State']).sum().reset_index()

    df = df.transpose().reset_index()
    df.columns = df.iloc[0,:]
    df.drop([0], axis = 0, inplace = True)
    df.reset_index(drop = True, inplace = True)
    df.rename(columns = {'Province_State' : 'Date'}, inplace = True)
    df.Date = pd.to_datetime(df.Date)

    df.drop(list(df.columns[1:][df.iloc[:,1:].sum(axis = 0) == 0]), axis = 1, inplace=True) 
    df.drop(['Grand Princess'], axis = 1, inplace = True)


    dfR = pd.DataFrame(np.empty_like(df))
    dfR.columns = df.columns
    dfR['Date'] = df['Date']
    
    
    for i in range(1, df.shape[1]):
        state = df.columns[i]
        j = np.where(df[state] > 0)[0][0]
        
        for m in range(j, df.shape[0]):
            if df.iloc[m, i] == 0:
                df.iloc[m, i] = df.iloc[m-1, i]

        dfR[state] = np.concatenate((np.full(j+5,np.nan), 
                                                pow(np.array(df[state][j+5:]) / np.array(df[state][j:df.shape[0]-5]), 1/5) - 1),
                                                axis = 0)  
    for i in range(1, dfR.shape[1]):
        s = [j for j in range(dfR.shape[0]) if not math.isnan(dfR.iloc[j,i])][0]
            
        for j in range(s+1, dfR.shape[0]-1):
            dfR.iloc[j, i] = np.mean([dfR.iloc[j-1, i],
                                                      dfR.iloc[j, i],
                                                      dfR.iloc[j+1, i]])
    return(dfR)

### World Confirmed
world_confirmed = pd.read_csv("JHU/time_series_covid19_confirmed_global.csv")
world_confirmedR = calculate_growth_rate_WORLD(world_confirmed)
### World Death
world_death = pd.read_csv("JHU/time_series_covid19_deaths_global.csv")
world_deathR = calculate_growth_rate_WORLD(world_death)
### World color
random.seed(125)

# colors = [f'rgba({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)},0.9)' for _ in range(world_confirmedR.shape[1]-1)]
# colors_World = pd.DataFrame({'country': world_confirmedR.columns[1:],
#                              'colors': colors})
# colors_World = colors_World.set_index('country').to_dict()['colors']
####
color_list = pd.read_csv("color_list.csv",)
color_list = color_list.append(color_list)
color_list.reset_index(drop = True, inplace = True)
colors = ['rgba(' + str(color_list['r'][x]) + ',' + str(color_list['g'][x]) + ',' + str(color_list['b'][x]) + ',' + str(0.9) + ')' for x in range(color_list.shape[0])]
colors_World = pd.DataFrame({'country': world_confirmedR.columns[1:],
                             'colors': colors[:len(world_confirmedR.columns[1:])]
                            })
colors_World = colors_World.set_index('country').to_dict()['colors']

### US Confirmed
us_confirmed = pd.read_csv("JHU/time_series_covid19_confirmed_US.csv")
us_confirmedR = calculate_growth_rate_US(us_confirmed)
us_confirmedR.drop('Diamond Princess', axis = 1, inplace = True)
### US Death
us_death = pd.read_csv("JHU/time_series_covid19_deaths_US.csv")
us_death.drop('Population', axis = 1, inplace = True)
us_deathR = calculate_growth_rate_US(us_death)
### US color
colors = [f'rgba({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)},0.9)' for _ in range(us_confirmedR.shape[1]-1)]
colors_US = pd.DataFrame({'state': us_confirmedR.columns[1:],
                             'colors': colors})
colors_US = colors_US.set_index('state').to_dict()['colors']


### Lockdown world
lockdown = pd.read_csv("covid19-lockdown-dates-by-country/countryLockdowndatesJHUMatch.csv")
lockdown = lockdown.drop(['Reference'], axis = 1)
lockdown = lockdown.groupby(['Country/Region']).min().reset_index()
lockdown['Date'] = pd.to_datetime(lockdown['Date'])
lockdown['Country/Region'].replace('Mainland China', 'China', inplace = True)
lockdown['Country/Region'].replace('The Bahamas', 'Bahamas', inplace = True)
lockdown['Country/Region'].replace('UK', 'United Kingdom', inplace = True)
lockdown['Type'].replace("Full", "Full lockdown", inplace = True)
lockdown['Type'].replace("Partial", "Partial lockdown", inplace = True)
lockdown['Type'].replace(np.nan, "Lockdown", inplace = True)


### Lockdown US
lockdown2 = pd.read_csv("lockdown_us.csv")
lockdown2 = lockdown2.drop(['Country','County'], axis = 1)
lockdown2 = lockdown2.groupby(['State']).min().reset_index()
lockdown2 = lockdown2.append(pd.Series(['Arkansas', np.nan, np.nan], index = lockdown2.columns), ignore_index=True)


####################################################################################
#######################   Page 3 - Plot1.   Survey      ##########################
####################################################################################
### original
concern = pd.read_csv('covid-19-polls-master/covid_concern_polls.csv')

concern.drop(['start_date','party','tracking','text','url'], axis = 1, inplace=True)
concern.replace(np.nan, 'Others', inplace=True)

concern_econ = concern[concern['subject'] == 'concern-economy']
concern_infec = concern[concern['subject'] == 'concern-infected']


### adjusted
concern_adj = pd.read_csv("covid-19-polls-master/covid_concern_polls_adjusted.csv")

concern_adj.drop(['modeldate','party','startdate','multiversions','tracking','timestamp','url'],
                axis = 1, inplace = True)
concern_adj.rename(columns = {'enddate': 'end_date'}, inplace = True)
concern_adj['end_date'] = pd.to_datetime(concern_adj['end_date'])

concern_adj['population'].replace('a', 'All Adults', inplace = True)
concern_adj['population'].replace('rv', 'Registered Voters', inplace = True)
concern_adj['population'].replace('lv', 'Likely Voters', inplace = True)

concern_adj_econ = concern_adj[concern_adj['subject'] == 'concern-economy']
concern_adj_infec = concern_adj[concern_adj['subject'] == 'concern-infected']

### topline
concern_topline = pd.read_csv('covid-19-polls-master/covid_concern_toplines.csv')

concern_topline.drop(['party', 'timestamp'], axis = 1, inplace = True)
concern_topline['modeldate'] = pd.to_datetime(concern_topline['modeldate'])

concern_topline_econ = concern_topline[concern_topline['subject'] == 'concern-economy']
concern_topline_infect = concern_topline[concern_topline['subject'] == 'concern-infected']

### Supportive accessories
symbols1 = pd.DataFrame({'pollster':concern_adj_econ.pollster.unique(),
                          'symbol': ['diamond','circle','cross', 
                                     'triangle-up','square','triangle-right',
                                     'diamond-tall','y-down',
                                     'x','hourglass',
                                     'star','hexagram'
                                    ]}).set_index('pollster').to_dict()['symbol']

sponsors = list(concern_econ.sponsor.unique())
sponsors = [sponsors[0]] + sponsors[2:len(sponsors)] + [sponsors[1]]
symbols2 = pd.DataFrame({'sponsor':sponsors,
                          'symbol': ['diamond','circle','cross', 
                                     'triangle-up','square','triangle-right',
                                     'diamond-tall','hourglass',
                                     'star','hexagram'
                                    ]}).set_index('sponsor').to_dict()['symbol']

symbols3 = pd.DataFrame({'population':['All Adults', 'Registered Voters', 'Likely Voters'],
                          'symbol': ['cross','hexagram','circle'
                                    ]}).set_index('population').to_dict()['symbol']


####################################################################################
#######################   Page 3 - Plot2.   Tweeter      ##########################
####################################################################################
daterange = pd.DataFrame(pd.date_range(start='3/22/2020',end='4/22/2020',freq='D'), columns = ['date'])
daterange['date'] = [x.timestamp() for x in daterange['date']]



####################################################################################
#######################   Page 4 - Plot1.   Unemployment      #####################
####################################################################################
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


####################################################################################
#######################   Page 5 - Plot1.   Legislation      ######################
####################################################################################
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


######################################################################################################################
######################################################################################################################
#################################         2.  APP Layout              ################################################
######################################################################################################################
######################################################################################################################


#########################################
###########  Initiate the app  ##########
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
local_stylesheets = ['style.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title="COVID19-visual_app_title"

#########################################
###########  Navigation  ################
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

#########################################
###########  Body Elements  #############
FLATTEN_THE_CURVE = [
    dbc.CardHeader(html.H5("Flatten The Curve")),
    dbc.CardBody([
        #dcc.Loading(),
        dcc.Tabs([
            dcc.Tab(label='World', children=[
                html.Div([
                    html.Label('Multi-Select Dropdown'),
                    dcc.Dropdown(
                        id = "selected_countries",
                        options=[{'label': x, 'value': x} for x in list(world_confirmedR.columns[1:])],
                        value= ['US','United Kingdom', 'Italy', 'Germany', 'Spain', 'South Korea', 'India', 'Austria'],
                        multi=True
                        ),
                    dcc.Dropdown(
                        id = "selected_measure",
                        options = [{'label': 'Confirmed Growth Rate', 'value': 'confirmed'},
                                   {'label': 'Death Growth Rate', 'value': 'death'}],
                        value = 'confirmed'
                        )

                ]),

                html.Div([
                    html.Label("my plot here"),
                    dcc.Graph(id = "lineplot1")
                    ]),
                
            ]),

            dcc.Tab(label='US', children=[
                html.Div([
                    html.Label('Multi-Select Dropdown'),
                    dcc.Dropdown(
                        id = "selected_states",
                        options=[{'label': x, 'value': x} for x in list(us_confirmedR.columns[1:])],
                        value= ['New York', 'California'],
                        multi=True
                        ),
                    dcc.Dropdown(
                        id = "selected_measure2",
                        options = [{'label': 'Confirmed Growth Rate', 'value': 'confirmed'},
                                   {'label': 'Death Growth Rate', 'value': 'death'}],
                        value = 'confirmed'
                        )

                ]),

                html.Div([
                    html.Label("my plot here"),
                    dcc.Graph(id = "lineplot2")
                    ]),
            ])

        ])

    ])


]

SURVEY_MEDIA = [
    dbc.CardHeader(html.H5("Survey")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H5("Select Topics :")
                ], width = 2),
            dbc.Col([
                dcc.Dropdown(
                    id = 'selected_question',
                    options = [{'label': 'How concerned are Americans about Infection?', 'value': 'Q_concern_infec'},
                               {'label': 'How concerned are Americans about Economy?', 'value': 'Q_concern_econ'},
                               {'label': 'Approval of Trump’s response varies widely by party', 'value': 'Q_approval_1'},
                               {'label': 'Do Americans approve of Trump’s response to the coronavirus crisis?', 'value': 'Q_approval_2'}]

                    )

                ], width = 10),

            ]),
        dbc.Row([
            dbc.Col([
                html.H5("Choose Filter :"),
                html.Img(src = "https://media.istockphoto.com/vectors/survey-satisfaction-scale-meter-emoticon-talk-bubbles-icons-vector-id1186938974?k=6&m=1186938974&s=170667a&w=0&h=JtfZXrP90BGvdKktvqM8dZsLauT2uyjRW9JoCF1PCkQ=",
                style = {"width" : '135px'})
                ], width = 2),
            dbc.Col([
                dcc.RadioItems(
                        id = 'radio_display1',
                        options=[{'label': 'All   ', 'value': 'All'},
                                {'label': 'By Pollster   ', 'value': 'by_pollster'},
                                {'label': 'By Sponsor  ', 'value': 'by_sponsor'},
                                {'label': 'By Population', 'value': 'by_population'}
                                ],
                        value='All',
                        labelStyle={'display': 'block'}, style={'fontSize': 14, 'marginTop': '5px'}
                        )

                ], width = 2),
            dbc.Col([
                dcc.Dropdown(
                                id = "selected_pollsters",
                                # options = [{'label': 'All', 'value': 'All'}] +
                                #           [{'label': x, 'value': x} for x in list(concern_adj_econ.pollster.unique())],
                                multi=True,
                                style={'height': '100px', 'marginTop': '10px'}
                                )

                ], width = 8)
            ]),


        dcc.Graph(id = "survey_plot1")


        ])

]

TWEETER = [
    dbc.CardHeader(html.H5('Tweeter HoT Words ')),
    dbc.CardBody([
        html.Div([
        html.Label('WordCloud', id='time-range-label'),
        html.Section(id="slideshow", children=[
            dcc.Slider(
                id='year-slider',
                updatemode = 'mouseup',
                min=daterange['date'].min(),
                max=daterange['date'].max(),
                value=daterange['date'].min(),
                marks={x: {'label' : str(pd.to_datetime(x, unit='s').date())} for x in daterange['date'].unique()},
                step=86400),
            html.Div(id="slide-container"),
            dbc.Row([
                dbc.Col([
                    html.Div(id="image")
                    ], width = 6),

                dbc.Col([
                    dcc.Graph(id ='hot-table', style={'display': 'inline-block'})
                    ], width = 6)

                ])
            
        ])
    ])

        ])

]

UNEMPLOYMENT = [
    dbc.CardHeader(html.H5("Unemployment")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                # slider - select date for map
                # html.P([
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
                        # ],  style = {
                        #             'width' : '87%',
                        #             'fontSize' : '20px',
                        #             'padding-left' : '60px',
                        #             'padding-right' : '100px',
                        #             'display': 'inline-block'
                        #             })

                ], width = 6),
            
            dbc.Col([
                # html.P([
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
                        # ],  style = {
                        #             'width' : '87%',
                        #             'fontSize' : '20px',
                        #             'padding-left' : '60px',
                        #             'padding-right' : '100px',
                        #             'display': 'inline-block'
                        #             })

                ], width = 6)

            ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='map')
                ], width = 6),
            dbc.Col([
                dbc.CardBody([
                    dbc.Row([dcc.Graph(id = 'plot1')]),
                    dbc.Row([dcc.Graph(id = 'plot2')])

                    ])
                ], width = 6),
            dbc.Col([
                # html.P([
                    html.Label("Select any states"),
                    dcc.Dropdown(id = 'opt', 
                                 options = opts,
                                 placeholder="Select any states",
                                 value = opts[0]['value'],                                 
                                 searchable=True,                              
                                 multi=True)
                        # ], style = {'width': '400px',
                        #             'fontSize' : '20px',
                        #             'padding-left' : '100px',
                        #             'display': 'inline-block'})

                ], width = 12)

            ])

        ])

]

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

######################################################
#################     Body    ########################
BODY = dbc.Container([

    dcc.Tabs([
        dcc.Tab(label='Overview', children=[
            dbc.Row([dbc.Col(dbc.Card(FLATTEN_THE_CURVE)),], style={"marginTop": 30})

            ]),
        dcc.Tab(label='Mobility', children=[

            ]),
        dcc.Tab(label='People Opinion', children=[
            dbc.Row([dbc.Col(dbc.Card(SURVEY_MEDIA)),], style={"marginTop": 30}),
            dbc.Row([dbc.Col(dbc.Card(TWEETER)),], style={"marginTop": 30})


            # dcc.Tabs([
            #     dcc.Tab(label='Survey', children=[
            #         dbc.Row([dbc.Col(dbc.Card(SURVEY_MEDIA)),], style={"marginTop": 30})

            #         ], className='custom-tab'),
            #     dcc.Tab(label='Tweeter', children=[
            #         ])


            #     ], vertical = True, parent_className='custom-tabs', className='custom-tabs-container')

            ]),

        dcc.Tab(label='Unemployment', children=[
            dbc.Row([dbc.Col(dbc.Card(UNEMPLOYMENT)),], style={"marginTop": 30})

            ]),

        dcc.Tab(label='Legislation', children=[
            dbc.Row([dbc.Col([dbc.Card(LEGAL_TABLE)])], style={"marginTop": 50})

            ]),

        ], colors={"border": "white", "primary": "gold", "background": "cornsilk"
    })
        
    ],
    className="mt-12",
)



app.layout = html.Div(children=[NAVBAR, BODY])


######################################################################################################################
######################################################################################################################
#################################         3.  CALLLBACKS             ################################################
######################################################################################################################
######################################################################################################################


####################################################################################
#######################   Page 1 - Plot1.   Flatten the Curve      ################
####################################################################################

@app.callback(dash.dependencies.Output("lineplot1", "figure"),
    [dash.dependencies.Input("selected_countries", "value"),
     dash.dependencies.Input("selected_measure", "value")])

def update_fig(selected_countries, selected_measure):

    data = []
    US = []
    IT = []
    GM = []
    SP = []
    SK = []
    ID = []
    UK = []

    if selected_measure == "confirmed":
        df = world_confirmedR
    elif selected_measure == "death":
        df = world_deathR

    if "US" in selected_countries:
        US = [go.Scatter(x = df.Date,
                             y = df['US'],
                             name = 'US',
                             mode = 'lines',
                             line = dict(color = 'rgba(53,92,125, 0.8)', width = 2, shape = 'spline'),
                             #text = ["United States" if i == 38 else "" for i in range(df.shape[0])],
                             #textposition = "top center",
                             #textfont = dict(color = "rgba(53,92,125, 1)")
                            ),
              go.Scatter(x = df.Date,
                          y = [df['US'][i] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == 'US'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
                          mode = 'markers',
                          marker = dict(color = 'rgba(53,92,125, 0.8)', size = 10),
                          #text = ["Partial" if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == 'US'].values[0]) == pd.Timestamp(df.Date[i]) else "" for i in range(df.shape[0])],
                          #textposition="top right",
                          #textfont = dict(color = "rgba(53,92,125, 1)")
                            )]
    
    if "Italy"  in selected_countries:
        IT = [go.Scatter(x = df.Date,
                             y = df['Italy'],
                             name = 'Italy',
                             mode = 'lines',
                             line = dict(color = 'rgba(153,184,152, 0.9)', width = 2, shape = 'spline'),
                            ),
              go.Scatter(x = df.Date,
                          y = [df['Italy'][i] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == 'Italy'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
                          mode = 'markers',
                          marker = dict(color = 'rgba(153,184,152, 0.9)', size = 10),
                            )]

    if "Spain" in selected_countries:
        SP = [go.Scatter(x = df.Date,
                             y = df['Spain'],
                             name = 'Spain',
                             mode = 'lines',
                             line = dict(color = 'rgba(237, 177, 131, 0.9)', width = 2, shape = 'spline'),
                            ),
              go.Scatter(x = df.Date,
                          y = [df['Spain'][i] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == 'Spain'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
                          mode = 'markers',
                          marker = dict(color = 'rgba(237, 177, 131, 0.9)', size = 10),
                          #text = ["Full" if lockdown.Date[lockdown['Country/Region'] == 'Spain'].values == df.Date[i] else "" for i in range(df.shape[0])],
                          #textposition="top right"
                            )]
    if "South Korea" in selected_countries:
        SK = [go.Scatter(x = df.Date,
                             y = df['South Korea'],
                             name = 'South Korea',
                             mode = 'lines',
                             line = dict(color = 'rgba(246,114,128, 0.9)', width = 2, shape = 'spline'),
                            ),
              go.Scatter(x = df.Date,
                          y = [df['South Korea'][i] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == 'South Korea'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
                          mode = 'markers',
                          marker = dict(color = 'rgba(246,114,128, 0.9)', size = 10),
                          #text = ["Full" if lockdown.Date[lockdown['Country/Region'] == 'South Korea'].values == df.Date[i] else "" for i in range(df.shape[0])],
                          #textposition="top right"
                            )]



    others1 = [go.Scatter(x = df.Date, 
                        y = df[selected_countries[i]],
                        name = selected_countries[i],
                        mode = 'lines',
                        line = dict(color = colors_World[selected_countries[i]], 
                            width = 1, shape = 'spline')) for i in range(len(selected_countries))]
    others2 = [go.Scatter(x = df.Date,
                          y = [df[selected_countries[i]][j] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == selected_countries[i]].values) == pd.Timestamp(df.Date.iloc[j]) else np.nan for j in range(df.shape[0])],
                          #name = selected_countries[i] + ' (' + str(lockdown.Type[lockdown['Country/Region'] == selected_countries[i]].values[0]) + ')',
                          mode = 'markers',
                          #marker = dict(color = colors_World[selected_countries[i]],  size = 5),
                          #text = [lockdown['Type'][lockdown['Country/Region'] == selected_countries[i]].values[0] if pd.to_datetime(lockdown.Date[lockdown['Country/Region'] == selected_countries[i]].values) == pd.Timestamp(df.Date.iloc[j]) else "unknown type" for j in range(df.shape[0])],
                          #textposition="top right"
                            ) for i in range(len(selected_countries))]

    

    data = data + others1 + others2 + US + IT + SP + SK + ID + GM + UK

    if selected_measure == "confirmed":
        layout = {"title": "Confirmed Case Growth Rate ", "height": 700, "plot_bgcolor": '#f5f7fa',}
    elif selected_measure == "death":
        layout = {"title": "Death Case Growth Rate", "height": 700, "plot_bgcolor": '#f5f7fa',}


    return dict(data = data,
                layout = layout)



@app.callback(dash.dependencies.Output("lineplot2", "figure"),
    [dash.dependencies.Input("selected_states", "value"),
     dash.dependencies.Input("selected_measure2", "value")])

def update_fig2(selected_states, selected_measure2):
    data = []
    NY = []
    CA = []


    if selected_measure2 == "confirmed":
        df = us_confirmedR
    elif selected_measure2 == "death":
        df = us_deathR

    if "New York" in selected_states:
        NY = [go.Scatter(x = df.Date,
                             y = df['New York'],
                             name = 'New York',
                             mode = 'lines',
                             line = dict(color = 'rgba(53,92,125, 0.9)', width = 3, shape = 'spline'),
                             #text = ["New York" if i == 38 else "" for i in range(df.shape[0])],
                             #textposition = "top center",
                             #textfont = dict(color = "rgba(53,92,125, 1)")
                            ),
              go.Scatter(x = df.Date,
                          y = [df['New York'][i] if pd.to_datetime(lockdown2.Date[lockdown2['State'] == 'New York'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
                          name = 'New York (lockdown)',
                          mode = 'markers',
                          marker = dict(color=[f'rgba({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)},0.9)'],
                       size=10),
                          #marker = dict(color = 'rgba(53,92,125, 1)', size = 10),
                          #text = ["Partial" if pd.to_datetime(lockdown2.Date[lockdown2['Country/Region'] == 'US'].values[0]) == pd.Timestamp(df.Date[i]) else "" for i in range(df.shape[0])],
                          #textposition="top right",
                          #textfont = dict(color = "rgba(53,92,125, 1)")
                            )]
    if "California" in selected_states:
        CA = [go.Scatter(x = df.Date,
                             y = df['California'],
                             name = 'California',
                             mode = 'lines+text',
                             line = dict(color = 'rgba(53,92,125, 0.9)', width = 3, shape = 'spline'),
                             text = ["California" if i == 38 else "" for i in range(df.shape[0])],
                             textposition = "top center",
                             textfont = dict(color = "rgba(53,92,125, 1)")
                            ),
              go.Scatter(x = df.Date,
                          y = [df['California'][i] if pd.to_datetime(lockdown2.Date[lockdown2['State'] == 'California'].values[0]) == pd.Timestamp(df.Date[i]) else np.nan for i in range(df.shape[0])],
                          name = 'California',
                          mode = 'markers',
                          marker = dict(color = 'rgba(53,92,125, 1)', size = 10),
                          #text = ["Partial" if pd.to_datetime(lockdown2.Date[lockdown2['Country/Region'] == 'US'].values[0]) == pd.Timestamp(df.Date[i]) else "" for i in range(df.shape[0])],
                          #textposition="top right",
                          #textfont = dict(color = "rgba(53,92,125, 1)")
                            )]

    others1 = [go.Scatter(x = df.Date, 
                        y = df[selected_states[i]],
                        name = selected_states[i],
                        mode = 'lines',
                        line = dict(color= f'rgba({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)},0.9)', 
                            width = 0.8, shape = 'spline')) for i in range(len(selected_states))]
    others2 = [go.Scatter(x = df.Date,
                          y = [df[selected_states[i]][j] if pd.to_datetime(lockdown2.Date[lockdown2['State'] == selected_states[i]].values) == pd.Timestamp(df.Date.iloc[j]) else np.nan for j in range(df.shape[0])],
                          name = selected_states[i] + ' (' + str(lockdown2.Type[lockdown2['State'] == selected_states[i]].values[0]) + ')',
                          mode = 'markers',
                          marker = dict(color = f'rgba({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)},0.9)', size = 5),
                          textposition="top right"
                            ) for i in range(len(selected_states))]

    data = data + others1 + others2 + NY + CA
    
    if selected_measure2 == "confirmed":
        layout = {"title": "Confirmed Case Growth Rate ", "height": 700, "plot_bgcolor": '#f5f7fa',}
    elif selected_measure2 == "death":
        layout = {"title": "Death Case Growth Rate", "height": 700, "plot_bgcolor": '#f5f7fa',}

    return dict(data = data,
                layout = layout)

####################################################################################
#######################   Page 3 - Plot1.   Survey      ###########################
####################################################################################
################ Survey Plot
### buttons
@app.callback(
    [Output('selected_pollsters', 'options'),
     Output('selected_pollsters', 'value')],
    [Input('radio_display1', 'value')])
def set_survey_options(which_one):
    if which_one == "All":
        return [[{'label': 'All', 'value': 'all'}], ['all']]
    elif which_one == "by_pollster":
        return [[{'label': x, 'value': x} for x in list(concern_adj_econ.pollster.unique())], ['Morning Consult']]
    elif which_one == "by_sponsor":
        return [[{'label': x, 'value': x} for x in sponsors], ['New York Times', 'CNBC', 'Fortune']]
    elif which_one == 'by_population':
        return [[{'label': x, 'value': x} for x in list(concern_adj_econ.population.unique())], ['All Adults', 'Registered Voters']]


@app.callback(
    Output('radio_display1', 'value'),
    [Input('radio_display1', 'options')])
def set_survey_value(available_options):
    return available_options[0]['value']


@app.callback(Output("survey_plot1", "figure"),
            [Input("selected_pollsters", "value"),
             Input("radio_display1", "value")])

def update_fig_s1(selected_pollsters, radio_display1):
    data = []
    topline = []
    All = []
    others1 = []
    others2 = []
    others3 = []
    others4 = []

    topline = [go.Scatter(x = concern_topline_econ.modeldate,
                             y = concern_topline_econ.very_estimate,
                             name = 'very (AVERAGE)',
                             mode = 'lines',
                             line = dict(color = "Red")
                            ),
               go.Scatter(x = concern_topline_econ.modeldate,
                             y = concern_topline_econ.somewhat_estimate,
                             name = 'somewhat (AVERAGE)',
                             mode = 'lines',
                             line = dict(color = "Pink")
                            ),
               go.Scatter(x = concern_topline_econ.modeldate,
                             y = concern_topline_econ.not_very_estimate,
                             name = 'not very (AVERAGE)',
                             mode = 'lines',
                             line = dict(color = "#B6D7B9")
                            ),
               go.Scatter(x = concern_topline_econ.modeldate,
                             y = concern_topline_econ.not_at_all_estimate,
                             name = 'not at all (AVERAGE)',
                             mode = 'lines',
                             line = dict(color = "Green")
                            )]


    if radio_display1 == 'All':
        All = [go.Scatter(x = concern_adj_econ.end_date,
                              y = concern_adj_econ.very_adjusted,
                              name = "very",
                              mode = 'markers',
                              marker = dict(size = concern_adj_econ.samplesize*0.005,
                                            color = "red",
                                            opacity = concern_adj_econ.weight / max(concern_adj_econ.weight)
                                           )),
               go.Scatter(x = concern_adj_econ.end_date,
                              y = concern_adj_econ.somewhat_adjusted,
                              name = "somewhat",
                              mode = 'markers',
                              marker = dict(size = concern_adj_econ.samplesize*0.005,
                                           color = "pink",
                                           opacity = concern_adj_econ.weight / max(concern_adj_econ.weight)
                                           )),
               go.Scatter(x = concern_adj_econ.end_date,
                              y = concern_adj_econ.not_very_adjusted,
                              name = "not_very",
                              mode = 'markers',
                              marker = dict(size = concern_adj_econ.samplesize*0.005,
                                           color = "#B6D7B9",
                                           opacity = concern_adj_econ.weight / max(concern_adj_econ.weight)
                                           )),
               go.Scatter(x = concern_adj_econ.end_date,
                              y = concern_adj_econ.not_at_all_adjusted,
                              name = "not_at_all",
                              mode = 'markers',
                              marker = dict(size = concern_adj_econ.samplesize*0.005,
                                           color = "Green",
                                           opacity = concern_adj_econ.weight / max(concern_adj_econ.weight)
                                           ))
                ]

    elif radio_display1 == 'by_pollster':
        others1 = [go.Scatter(x = concern_adj_econ[concern_adj_econ['pollster'] == selected_pollsters[i]].end_date, 
                              y = concern_adj_econ[concern_adj_econ['pollster'] == selected_pollsters[i]].very_adjusted,
                                name = 'very ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = [x+5 if x<3 else x for x in concern_adj_econ.samplesize*0.006],
                                            color = "red",
                                            opacity = [x+0.1 if x<0.5 else x for x in concern_adj_econ.weight / max(concern_adj_econ.weight)],
                                            symbol = symbols1[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]
        others2 = [go.Scatter(x = concern_adj_econ[concern_adj_econ['pollster'] == selected_pollsters[i]].end_date, 
                              y = concern_adj_econ[concern_adj_econ['pollster'] == selected_pollsters[i]].somewhat_adjusted,
                                name = 'somewhat ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = [x+5 if x<3 else x for x in concern_adj_econ.samplesize*0.006],
                                            color = "pink",
                                            opacity = [x+0.1 if x<0.5 else x for x in concern_adj_econ.weight / max(concern_adj_econ.weight)],
                                            symbol = symbols1[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]
        others3 = [go.Scatter(x = concern_adj_econ[concern_adj_econ['pollster'] == selected_pollsters[i]].end_date, 
                              y = concern_adj_econ[concern_adj_econ['pollster'] == selected_pollsters[i]].not_very_adjusted,
                                name = 'not very ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = [x+5 if x<3 else x for x in concern_adj_econ.samplesize*0.006],
                                            color = "#B6D7B9",
                                            opacity = [x+0.1 if x<0.5 else x for x in concern_adj_econ.weight / max(concern_adj_econ.weight)],
                                            symbol = symbols1[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]
        others4 = [go.Scatter(x = concern_adj_econ[concern_adj_econ['pollster'] == selected_pollsters[i]].end_date, 
                              y = concern_adj_econ[concern_adj_econ['pollster'] == selected_pollsters[i]].not_at_all_adjusted,
                                name = 'not at all ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = [x+5 if x<3 else x for x in concern_adj_econ.samplesize*0.006],
                                            color = "green",
                                            opacity = [x+0.1 if x<0.5 else x for x in concern_adj_econ.weight / max(concern_adj_econ.weight)],
                                            symbol = symbols1[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]

    elif radio_display1 == 'by_sponsor':
        others1 = [go.Scatter(x = concern_econ[concern_econ['sponsor'] == selected_pollsters[i]].end_date, 
                              y = concern_econ[concern_econ['sponsor'] == selected_pollsters[i]].very,
                                name = 'very ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = 8,
                                            color = "red",
                                            opacity = 0.8,
                                            symbol = symbols2[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]
        others2 = [go.Scatter(x = concern_econ[concern_econ['sponsor'] == selected_pollsters[i]].end_date, 
                              y = concern_econ[concern_econ['sponsor'] == selected_pollsters[i]].somewhat,
                                name = 'somewhat ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = 8,
                                            color = "pink",
                                            opacity = 0.8,
                                            symbol = symbols2[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]
        others3 = [go.Scatter(x = concern_econ[concern_econ['sponsor'] == selected_pollsters[i]].end_date, 
                              y = concern_econ[concern_econ['sponsor'] == selected_pollsters[i]].not_very,
                                name = 'not very ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = 8,
                                            color = "#B6D7B9",
                                            opacity = 0.8,
                                            symbol = symbols2[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]
        others4 = [go.Scatter(x = concern_econ[concern_econ['sponsor'] == selected_pollsters[i]].end_date, 
                              y = concern_econ[concern_econ['sponsor'] == selected_pollsters[i]].not_at_all,
                                name = 'not at all ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = 8,
                                            color = "green",
                                            opacity = 0.8,
                                            symbol = symbols2[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]

    elif radio_display1 == 'by_population':
        others1 = [go.Scatter(x = concern_adj_econ[concern_adj_econ['population'] == selected_pollsters[i]].end_date, 
                              y = concern_adj_econ[concern_adj_econ['population'] == selected_pollsters[i]].very_adjusted,
                                name = 'very ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = 6,
                                            color = "red",
                                            opacity = 0.8,
                                            symbol = symbols3[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]
        others2 = [go.Scatter(x = concern_adj_econ[concern_adj_econ['population'] == selected_pollsters[i]].end_date, 
                              y = concern_adj_econ[concern_adj_econ['population'] == selected_pollsters[i]].somewhat_adjusted,
                                name = 'somewhat ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = 6,
                                            color = "pink",
                                            opacity = 0.8,
                                            symbol = symbols3[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]
        others3 = [go.Scatter(x = concern_adj_econ[concern_adj_econ['population'] == selected_pollsters[i]].end_date, 
                              y = concern_adj_econ[concern_adj_econ['population'] == selected_pollsters[i]].not_very_adjusted,
                                name = 'not very ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = 6,
                                            color = "#B6D7B9",
                                            opacity = 0.8,
                                            symbol = symbols3[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]
        others4 = [go.Scatter(x = concern_adj_econ[concern_adj_econ['population'] == selected_pollsters[i]].end_date, 
                              y = concern_adj_econ[concern_adj_econ['population'] == selected_pollsters[i]].not_at_all_adjusted,
                                name = 'not at all ' + '(' + selected_pollsters[i] + ')',
                                mode = 'markers',
                                marker = dict(size = 6,
                                            color = "green",
                                            opacity = 0.8,
                                            symbol = symbols3[selected_pollsters[i]]
                                           )
                                ) for i in range(len(selected_pollsters))]

    data = topline + All + others1 + others2 + others3 + others4

    layout = dict(title = {
                    'text': "<b>How concerned are Americans about economy?</b>",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                   plot_bgcolor='rgb(247,245,245)',
                   height = 500,
                   hovermode='closest',
                   xaxis_showgrid=False, yaxis_showgrid=False,
                   )

    return dict(data = data,
                layout = layout)




####################################################################################
#######################   Page 3 - Plot2.   Tweeter      ###########################
####################################################################################
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


####################################################################################
#######################   Page 4 - Plot1.   Unemployment      ######################
####################################################################################

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

layout1 = go.Layout(title = 'Time Series for Unemployment Rate',
                   hovermode = 'x',
                   spikedistance =  -1,
                   xaxis=dict(
                       showticklabels=True,
                       spikemode  = 'across+toaxis',
                       linewidth=0.5,
                       mirror=True)                       
                       )
layout2 = go.Layout(title = 'Time Series for the Emerging Unemployment Claims',
                   hovermode = 'x',
                   spikedistance =  -1,
                   xaxis=dict(
                       showticklabels=True,
                       spikemode  = 'across+toaxis',
                       linewidth=0.5,
                       mirror=True))

####################################################################################
#######################   Page 5 - Plot1.   Legislation      ######################
####################################################################################

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
    app.run_server(debug=True)