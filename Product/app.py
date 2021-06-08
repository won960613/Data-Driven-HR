#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, send_from_directory
from dash import Dash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import dash_html_components as html

server=Flask(__name__, static_url_path='')
dash_app=Dash(__name__, server=server, url_base_pathname='/dashboard/')
dash_app.layout = html.Div([html.H1('Hi there, I am app1 for dashboards')])
@server.route("/")
def root():
    return server.send_static_file('index.html')

@server.route('/dashboard')
def render_dashboard():
    return flask.redirect('/dash1')

app=DispatcherMiddleware(server, {
    '/dash1':dash_app.server
})

if __name__=="__main__":
    server.run()

