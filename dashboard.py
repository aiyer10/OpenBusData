import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import glob, os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

folder = r'/path/to/files'
print("Reading files")
result = pd.DataFrame()
for x in glob.glob(os.path.join(folder, r'*.csv')):
    print(x)
    df = pd.read_csv(x)
    df = df[df['Operator']=='SCCM']
    result = pd.concat([result, df], ignore_index=True)

result['Time'] = pd.to_datetime(result['Time'])
result['Day'] = result['Time'].dt.date

print("Drawing maps...")
fig = px.scatter_mapbox(result, lat="Latitude", lon="Longitude", hover_name="Operator",color='Day', hover_data=["Operator", "Time"], zoom=5)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

print("Done")
if __name__ == '__main__':
    app.run_server(debug=True)
