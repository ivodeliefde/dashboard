# -*- coding: utf-8 -*-
import os
import dash
from dash_skeleton import prettyDash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import requests
import json
import pandas as pd
from requests.auth import HTTPBasicAuth

# Globals
mapbox_access_token = os.getenv("MAPBOX_ACCESS_TOKEN")
user = os.getenv("geoserver_user")
password = os.getenv("geoserver_password")

# Retrieving and preparing data 
r = requests.get("https://ivo-data.com/geoserver/ivodata/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=ivodata:positionsfound&outputFormat=application%2Fjson", auth=HTTPBasicAuth(user, password))
long,lat,t = [],[],[]
geojson = json.loads(r.text)

for feature in geojson["features"]:
	long.append(feature["geometry"]["coordinates"][0])
	lat.append(feature["geometry"]["coordinates"][1])
	t.append(feature["properties"]["time"])
df = pd.DataFrame([long,lat,t], ["longitude","latitude","time"]).T

map_data = [ go.Scattermapbox(
			lon = df['longitude'],
			lat = df['latitude'],
			mode = 'markers',
			marker = dict(
				size = 8,
				opacity = 0.8
				)
			)
		]

map_layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=51.8324,
            lon=5.2483
        ),
        pitch=0,
        zoom=17
    ),
)

graph_data = [ go.Histogram(
			x = df['time']
		)
	]
graph_layout = []

# Layout functions
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

# App layout and defining graphs
app = prettyDash()

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)
 
app.layout = html.Div(
	className="container",
	children=[
		html.Div(
			className="row",
			children = [ 
				html.Div(
					children=[
						dcc.Markdown('''# Dashboard Indoor Wayfinding

An online dashboard with indoor wayfinding statistics for API endpoint [geographicapi.herokuapp.com/get_pos](https://geographicapi.herokuapp.com/get_pos).''')		
					]
				)
			]
		),
		html.Div(
			className="row",
			children = [
				html.Div(
					children=[
						dcc.Graph(
							id='map',
							figure={
								'data': map_data,
								'layout': map_layout
							}
						)
					]
				)
			]
		),
		html.Div(
			className="row",
			children = [
				html.Div(
					children=[
						dcc.Graph(
							id='linegraph',
							figure={
								'data': graph_data,
								'layout': graph_layout
							}
						)
					]
				)
			]
		),
		html.Div(
			className="row",
			children = [
				generate_table(df)
			]
		)
	]
)

if __name__ == '__main__':
    app.run_server(debug=True)