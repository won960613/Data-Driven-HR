import json

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

import plotly.express as px
import pandas as pd
import os

app = dash.Dash(__name__)
server = app.server


# ###################### DATA PREPROCESSING ######################
# Load data
root = os.path.join(os.getcwd(), 'DATA')
df = pd.read_csv(os.path.join(root, 'data_for_dash.csv'), index_col = 0)
elements, stylesheet = [], []

# -------------------------------- STYLESHEET --------------------------------
# -- Group selector
stylesheet.append({'selector': 'node',
                   'style': {'content': 'data(label)'}
                  })
# -- Class selector
stylesheet.append({'selector': '.root',
                   'style': {'background-color': 'blue'}
                  })
stylesheet.append({'selector': '.A',
                   'style': {'width': 'data(size)',
                             'height': 'data(size)'}
                  })
stylesheet.append({'selector': '.program',
                   'style': {'width': 'data(size)',
                             'height': 'data(size)'}
                  })

# Set Jikwon info
selected_jikwon = int(6163718)
data = df[df['JIKWON_NO'] == selected_jikwon]
selected_name = data['NAME'].unique()[0].rstrip()

# create nodes
elements=[]
# -- Jikwon Node
elements.append({'data': {'id': selected_name, 'label': selected_name},
                 'classes': 'root',
                 'position': {'x': 150, 'y': 150},
                 'grabbable': False})
# -- Program Nodes
for name in list(data['A'].unique()):
    elements.append({'data': {'id': name, 'label': name, 'size': data[data["A"] == name]["A"].count()},
                     'classes': 'A'})

for name in list(data['프로그램종류'].unique()):
    elements.append({'data': {'id': name, 'label': name, 'size': data[data["프로그램종류"] == name]["프로그램종류"].count()},
                     'classes': 'program'})

# create edges
for t in list(data['A'].unique()):
    elements.append({'data': {'source': selected_name, 'target': t}})

for f, t in zip(list(data['A']), list(data['프로그램종류'])):
    elements.append({'data': {'source': f, 'target': t}})

# ################################# APP LAYOUT ################################
styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(50% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {'height': 'calc(98vh - 80px)'}
}

app.layout = html.Div([
    html.Div(className='eight columns', children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=elements,
            stylesheet=stylesheet,
            style={
                'height': '95vh',
                'width': '100%'
            }
        )
    ]),

    html.Div(className='four columns', children=[
        dcc.Tabs(id='tabs', children=[
            dcc.Tab(label='Control Panel', children=[
                
            ]),

            dcc.Tab(label='JSON', children=[
                html.Div(style=styles['tab'], children=[
                ])
            ])
        ]),

    ])
])


# ############################## CALLBACKS ####################################



if __name__ == '__main__':
    app.run_server(debug=True)