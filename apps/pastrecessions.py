import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
from pytrends.request import TrendReq
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
from app import app
from apps import sidebar
import yfinance as yf
#fct
fig = make_subplots(rows = 1, cols = 2, subplot_titles = ('Internet crisis (2001)', 'Subprime crisis (2008)'))
data = yf.download('^DJI')['Adj Close']
ret_now = data.loc['2020-01-30':].pct_change()[1:]
# 2007_209 
ret_2007_2009 = data.loc['2007-01-03':'2009-12-31'].pct_change()[1:]
cum_ret_2007_2009 = np.cumprod(1 + ret_2007_2009) - 1
ret_now_tmp = pd.DataFrame()
ret_now_tmp['ret'] = range(len(ret_2007_2009))
ret_now_tmp['ret'][0:51] = ret_now
ret_now_tmp['ret'][51:] = np.nan
cum_ret_now = np.cumprod(1 + ret_now_tmp) - 1
fig.add_trace(go.Scatter(x = ret_2007_2009.index, y = cum_ret_2007_2009, mode = 'lines', name = 'ret_2007_2009'), row = 1, col = 2)
fig.add_trace(go.Scatter(x = ret_2007_2009.index, y = cum_ret_now['ret'], mode = 'lines', name = 'ret_now'), row = 1, col = 2)
# Bulle internet (Mars - Nov 2001)
ret_2001 = data.loc['2001-03-01':'2001-11-30'].pct_change()[1:]
cum_ret_ret_2001 = np.cumprod(1 + ret_2001) - 1
ret_now_tmp = pd.DataFrame()
ret_now_tmp['ret'] = range(len(ret_2001))
ret_now_tmp['ret'][0:51] = ret_now
ret_now_tmp['ret'][51:] = np.nan
cum_ret_now = np.cumprod(1 + ret_now_tmp) - 1
fig.add_trace(go.Scatter(x = ret_2001.index, y = cum_ret_ret_2001, mode = 'lines', name = 'ret_2007_2009'), row = 1, col = 1)
fig.add_trace(go.Scatter(x = ret_2001.index, y = cum_ret_now['ret'], mode = 'lines', name = 'ret_now'), row = 1, col = 1)
#FIGURE SLIDE COMPARAIRAISON
layout = html.Div([
    sidebar.sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'50em'}),
                html.H4('FINANCIAL IMPACT OF COVID-19',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px','color':'rgb(87, 88, 90)','font-weight':'bolder'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('CORONAVIRUS IMPACT')],href ='/finance',className = "sousOnglet"),
                            ]
                        ), 
                        dbc.Row(
                            [
                                html.A([html.Div('RECESSIONS COMPARISON'),html.Div(className='encoche',style={'top':'213px','margin-top':'0px'})],href ='/finance/compare',className = "sousOngletActived")
                            ]
                        ), 
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row("dada",style={'color':'white','margin-left':'2em','margin-top':'1em'}),
                    dcc.Loading(
                        dcc.Graph(id='trend',figure=fig,style={'height':'800px'}),
                        type='circle'
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])

#CALLBACKS
