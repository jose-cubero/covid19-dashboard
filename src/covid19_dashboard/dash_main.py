# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
pd.options.plotting.backend = "plotly"

# local imports
from .data_parser.covid_JHU import get_clean_covid_data

def launch_server():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    df = get_clean_covid_data('confirmed').T

    fig = df.plot( )
    fig2 = fig

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        ),
        dcc.Graph(
            id='example-graph2',
            figure=fig2
        )
    ])
    
    print("Starting server app")
    app.run_server(debug=True)
    print("Closing server app")

if __name__ == '__main__':
    launch_server()
