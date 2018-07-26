# -*- coding: utf-8 -*-
import os
import asyncio
import dash
from dash_skeleton import prettyDash
from app_layout import get_app_layout

# App layout and defining graphs
app = prettyDash()

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)

app.layout = get_app_layout()

if __name__ == '__main__':
    app.run_server(debug=True)