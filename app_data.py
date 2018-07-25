import os
import json
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import plotly.graph_objs as go

def get_app_data():
	# Globals
	mapbox_access_token = os.getenv("MAPBOX_ACCESS_TOKEN")
	user = os.getenv("geoserver_user")
	password = os.getenv("geoserver_password")
	url = "https://ivo-data.com/geoserver/ivodata/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=ivodata:positionsfound&outputFormat=application%2Fjson"

	# Retrieve data
	r = requests.get(url, auth=HTTPBasicAuth(user, password))
	geojson = json.loads(r.text)

	# DataFrame
	long,lat,t = [],[],[]
	for feature in geojson["features"]:
		long.append(feature["geometry"]["coordinates"][0])
		lat.append(feature["geometry"]["coordinates"][1])
		t.append(feature["properties"]["time"])
	df = pd.DataFrame([long,lat,t], ["longitude","latitude","time"]).T

	# Map 
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

	# Histogram 
	graph_data = [ go.Histogram(
				x = df['time']
			)
		]
		
	graph_layout = []
	
	return df, map_data, map_layout, graph_data, graph_layout