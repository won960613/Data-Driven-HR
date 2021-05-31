# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# set data
root = os.path.join(os.getcwd(), 'DATA')
df = pd.read_csv(os.path.join(root, 'data_for_dash.csv'), index_col = 0)
elements = []

# 글!
markdown_text = '''
### 마크다운으로 텍스트 작성 가능
> test  
**행번 6163718** 직원 데이터  
'''
    
app.layout = html.Div(children=[
    html.H1(children='Data Driven HRM',
            style={'textAlign': 'center'}),
    
    dcc.Input(
        id='ibx',
        placeholder='직원번호 검색',
        type='text',
        value=''
    ),
    html.Button('조회', id='btn'),
    
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='업무 네트워크', value='tab-1'),
        dcc.Tab(label='관계도 네트워크', value='tab-2'),
    ]),
    
    html.Div(id='tabs-content'), 

    dcc.Markdown(children=markdown_text)
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
                cyto.Cytoscape(id='cytoscape',
                               elements=elements,
                               layout={'name': 'cose'},
                               style={'width': '1100px', 'height': '500px'})
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])

@app.callback(
    dash.dependencies.Output('cytoscape', 'elements'),
    [dash.dependencies.Input('btn', 'n_clicks')],
    [dash.dependencies.State('ibx', 'value')])
def update_output(n_clicks, value):
    if value == "" or int(value) not in (df['JIKWON_NO'].unique()):
        return []
    selected_jikwon = int(value)
    data = df[df['JIKWON_NO'] == selected_jikwon]
    selected_name = data['NAME'].unique()[0].rstrip()

    elements=[]
    # create nodes
    elements.append({'data': {'id': selected_name, 'label': selected_name},
                    'position': {'x': 150, 'y': 150},
                    'grabbable': False,
                    'classes': 'blue',
                    'size': 50})
    for name in list(data['A'].unique()) + list(data['프로그램종류'].unique()):
        elements.append({'data': {'id': name, 'label': name}})

    # create edges
    for t in list(data['A'].unique()):
        elements.append({'data': {'source': selected_name, 'target': t}})

    for f, t in zip(list(data['A']), list(data['프로그램종류'])):
        elements.append({'data': {'source': f, 'target': t}})

    return elements


if __name__ == '__main__':
    app.run_server(debug=True)  # automatically refresh page when code is changed