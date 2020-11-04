# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# local imports
import covid19_dashboard.data_parser.covid_JHU as jhu

def foo():
    print("in foo context.")

def launch_server():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    df = jhu.parse_timeseries_csv('confirmed')
    # available_indicators = df['Indicator Name'].unique()

    fig = px.line(df, x='Date', y='Value', color='Country')

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        ),
        # dcc.Graph(
        #     id='example-graph2',
        #     figure=fig2
        # )
    ])
    
    print("Starting server app")
    app.run_server(debug=True)
    print("Closing server app")

if __name__ == '__main__':
    print ("in main context.")
    launch_server()

