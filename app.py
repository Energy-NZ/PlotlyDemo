# app.py
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

# Sample data
data = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 15, 13, 17, 14]
})

# Create figure
fig = px.line(data, x="x", y="y", title="Basic Plotly Line Chart in Dash")

# Initialize Dash app
app = Dash(__name__)
server = app.server  # for Render / Azure

# Layout
app.layout = html.Div(children=[
    html.H1("Energy NZ Dash"),
    dcc.Graph(id='example-graph', figure=fig)
])

# Run locally
if __name__ == "__main__":
    app.run(debug=True)

