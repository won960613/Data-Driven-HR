import dash
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_core_components as dcc
import random

app = dash.Dash(__name__)
# app.layout = html.H1('hello dash')
app.layout = html.Div(
    [
        html.Button('create ramdom number',
                    id='button1',
                    style={'display': 'block', 'padding': '5', 'backgroud-color': '#aabbcc'}
                    ),
        html.Label('...',
                   id='label1',
                   style={'display': 'inline-block', 'margin': '10'}
                   ),

        dcc.Graph(id='graph1')
    ]
)

'''
# 버튼 클릭 이벤트를 update_output 함수로, 함수이 실행결과를 label1 요소로 묶는 기능
@app.callback(
    Output(component_id='label1', component_property='children'),
    [Input(component_id='button1', component_property='n_clicks')]
)
def update_output(input_value):
    return random.random()
'''

@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='button1', component_property='n_clicks')]
)
def update_output(input_value):
    random_x = [i for i in range(5)]
    random_y = [random.random() for _ in  range(5)]
    figure = {
        'data':[
            {'x':random_x, 'y':random_y, 'type': 'bar', 'name': 'Series1'}
        ],
        'layout':{
            'title': 'Dash Data Visualization'
        }
    }

    return figure


if __name__ == '__main__':
    app.run_server(debug=True, port=8080, host='0.0.0.0')
