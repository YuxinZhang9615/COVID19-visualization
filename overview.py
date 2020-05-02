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

#################################################################        Data       #############################################################
##############################      Plot 1      #################
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




#################################################   Reaction Callback   ################################################
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
