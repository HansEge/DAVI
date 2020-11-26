import json
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# import dash_bootstrap_components as dbc

app=dash.Dash()

app.layout = html.Div([
                dcc.Graph(id='graph',figure={}),
                html.Pre(id='relayout-data'),
                dcc.Graph(id='graph2', figure={})])

# Just to see what values are captured.
@app.callback(Output('relayout-data', 'children'),
              [Input('graph', 'relayoutData')])
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


@app.callback(Output('graph2', 'figure'),
             [Input('graph', 'relayoutData')],
             [State('graph2', 'figure')])
def graph_event(select_data,  fig):
    try:
       fig['layout'] = {'xaxis':{'range':[select_data['xaxis.range[0]'],select_data['xaxis.range[1]']]}}
    except KeyError:
       fig['layout'] = {'xaxis':{'range':['zoomed out value']}}
    return fig

app.run_server()