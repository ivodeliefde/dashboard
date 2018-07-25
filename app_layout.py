import dash_core_components as dcc
import dash_html_components as html
from app_data import get_app_data

# HTML generator functions
def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )

def generate_row(children):
	return html.Div(
					className = "row",
					children = children
				)

def generate_graph(width="twelve",**kwargs):
	return html.Div(
			className="{} columns".format(width),
			children = [
				dcc.Graph(**kwargs)
				]
			)

# Page to be rendered			
def get_app_layout():
	df, map_data, map_layout, graph_data, graph_layout = get_app_data()	
	return html.Div(
			className="container",
			children=[
				generate_row([ 
						html.Div(
							children=[
								dcc.Markdown('''# Dashboard Indoor Wayfinding

An online dashboard with indoor wayfinding statistics for API endpoint [geographicapi.herokuapp.com/get_pos](https://geographicapi.herokuapp.com/get_pos).''')		
							]
						)
					]
				),
				generate_row([
						generate_graph(
							id='map',
							figure={
								'data': map_data,
								'layout': map_layout
							}
						)
					]
				),
				generate_row([
						generate_graph(
							id='linegraph',
							figure={
								'data': graph_data,
								'layout': graph_layout
							}
						)
					]
				),
				generate_row([
						generate_table(df)
					]
				)
			]
		)
