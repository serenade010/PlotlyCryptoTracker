import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
import pandas as pd
import plotly.express as px
from pandas import json_normalize
import plotly.graph_objects as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

isPricingChart = True


def fetch_data(symbol, chart):
    response = requests.get(
        f" https://min-api.cryptocompare.com/data/v2/histoday?fsym={symbol}&tsym=USD&limit=100")

    data = response.json()
    df = json_normalize(data['Data']['Data'])
    df = df.drop(columns=['conversionType', 'conversionSymbol'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return draw_plot(df, chart)


def draw_plot(df, chart):
    if chart == 'candle':
      
      fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

    else:
        fig = px.line(df, x='time', y="close")

    return fig




app.layout = html.Div([
    html.Div([
        html.Div([

            html.H3("Select Symbol"),
            dcc.Dropdown(

                id='symbol-dropdown',
                options=[
                    {'label': 'Bitcoin', 'value': 'BTC'},
                    {'label': 'Ethereum', 'value': 'ETH'},
                    {'label': 'Binance Coin', 'value': 'BNB'}
                ],
                className="symbol-drop",
                value='BTC'
            ),
            html.H3("Select Chart"),
            dcc.Dropdown(

                id='chart-dropdown',
                options=[
                    {'label': 'Price Chart', 'value': 'price'},
                    {'label': 'Candlestick Chart', 'value': 'candle'},

                ],
                className="chart-drop",
                value='price'
            ),
            html.H3("Chart Configuration"),
           
        ], className="dropdown-container"),
    ],
        className="menu",

    ),
    html.Div([
        dcc.Graph(
            id='main-graph',
            figure=fetch_data("BTC", 'price'),
        )], className="main"
    ),
], className="container")


@app.callback(
    Output('main-graph', 'figure'),
    Input('symbol-dropdown', 'value'),
    Input('chart-dropdown', 'value'))
def update_graph(symbol, chart):
    return fetch_data(symbol, chart)


if __name__ == '__main__':
    app.run_server(debug=True)
