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

def get_dash_app():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    # df = jhu.parse_timeseries_csv('confirmed')
    # df = jhu.get_covid_data_all().loc[:, ['Date', 'Location', 'Confirmed', 'Entry_Type']]
    df = jhu.get_covid_data_all()
    df = df[df['Entry_Type'] == 'un_region']
    # available_indicators = df['Indicator Name'].unique()

    # fig = px.area(df, x='Date', y=['Confirmed'], color='Location',title="Graph 0 tittle", facet_col='Continent')
    fig = px.area(df, x='Date', y=['Confirmed', 'Deaths'], color='Location',title="Graph 0 tittle", facet_col='Continent')

    app.layout = html.Div(children=[
        html.H1(children='COVID-19 Timelines'),

        html.H4(children='''
            A tool for data analysis. THIS TEXT CONTINUES HERE...
        '''),

        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='MTL'
        ), 
        dcc.Graph(
            id='graph1',
            figure=fig
        )
           
            # dcc.Graph(
            #     id='example-graph2',
            #     figure=fig2
            # )
        ],
        # style={'width': '50%','padding-left':'25%', 'padding-right':'25%'},
        # style={"display": "inline-block"}
#         style={"display": "inline-block", "grid-template-columns": "20% 80%", }
    )
    
    # print("Starting server app")
    # app.run_server(debug=True)
    # print("Closing server app")
    return app

def launch_server():
    app=get_dash_app()
    app.run_server(debug=True)

if __name__ == '__main__':
    print ("in main context.")
    launch_server()




##### Saved forlater
        # children=[dcc.Graph(
        #     id='histogram-graph',
        #     figure={
        #         'data': [{
        #             'x': df['complaint_type'],
        #             'text': df['complaint_type'],
        #             'customdata': df['key'],
        #             'name': '311 Calls by region.',
        #             'type': 'histogram'
        #         }],
        #         'layout': {
        #             'title': 'NYC 311 Calls category.',
        #             'height': 500,
        #             'padding': 150
        #         }