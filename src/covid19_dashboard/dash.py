# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
pd.options.plotting.backend = "plotly"

# local imports
from covid_JHU import get_clean_covid_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = get_clean_covid_data('confirmed').T
print(df)

# see https://plotly.com/python/px-arguments/ for more options
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
# fig = px.scatter(df, x="City", y="Amount", color="Fruit", barmode="group")
# fig = px.scatter(df, x="City", y="Amount", color="Fruit", barmode="group")
fig = df.plot()
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

def launch_server():
    app.run_server(debug=True)

if __name__ == '__main__':
    launch_server