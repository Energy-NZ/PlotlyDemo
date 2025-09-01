# dash_plotly_demo.py

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

# Sample data
data = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 15, 13, 17, 14]
})

# Create a Plotly figure
fig = px.line(data, x="x", y="y", title="Basic Plotly Line Chart in Dash")

# Initialize the Dash app
app = dash.Dash(__name__)
# Expose the server for Azure deployment
server = app.server

# Layout of the app
app.layout = html.Div(children=[
    html.H1(children="Hello Dash!"),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

