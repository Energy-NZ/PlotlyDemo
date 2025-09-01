import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Create sample data with fixed values
dates = pd.date_range('2023-01-01', periods=100, freq='D')

# Generate deterministic sales data
sales_values = []
base_sales = 1000
for i in range(100):
    # Create variation using simple math patterns
    daily_variation = (i % 7 - 3) * 50 + (i % 30 - 15) * 20
    base_sales += daily_variation
    sales_values.append(max(500, base_sales))  # Ensure minimum sales

# Create product and region assignments using index patterns
products = ['Product A', 'Product B', 'Product C']
regions = ['North', 'South', 'East', 'West']

sales_data = pd.DataFrame({
    'date': dates,
    'sales': sales_values,
    'product': [products[i % 3] for i in range(100)],
    'region': [regions[i % 4] for i in range(100)]
})

# Initialize the Dash app
app = dash.Dash(__name__)
# Expose the server for Azure deployment
server = app.server

# Define the layout
app.layout = html.Div([
    html.H1("Sales Dashboard", style={'text-align': 'center', 'margin-bottom': '30px'}),
    
    # Controls
    html.Div([
        html.Div([
            html.Label("Select Product:"),
            dcc.Dropdown(
                id='product-dropdown',
                options=[{'label': product, 'value': product} 
                        for product in sales_data['product'].unique()],
                value=sales_data['product'].unique().tolist(),
                multi=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Select Region:"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} 
                        for region in sales_data['region'].unique()],
                value=sales_data['region'].unique().tolist(),
                multi=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], style={'margin-bottom': '30px'}),
    
    # Charts
    html.Div([
        html.Div([
            dcc.Graph(id='sales-time-series')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='sales-by-product')
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),
    
    html.Div([
        html.Div([
            dcc.Graph(id='sales-by-region')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='sales-heatmap')
        ], style={'width': '50%', 'display': 'inline-block'})
    ])
])

# Callback for updating charts
@app.callback(
    [Output('sales-time-series', 'figure'),
     Output('sales-by-product', 'figure'),
     Output('sales-by-region', 'figure'),
     Output('sales-heatmap', 'figure')],
    [Input('product-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_charts(selected_products, selected_regions):
    # Filter data
    filtered_data = sales_data[
        (sales_data['product'].isin(selected_products)) &
        (sales_data['region'].isin(selected_regions))
    ]
    
    # Time series chart
    time_series_fig = px.line(
        filtered_data, 
        x='date', 
        y='sales', 
        color='product',
        title='Sales Over Time'
    )
    time_series_fig.update_layout(height=400)
    
    # Sales by product
    product_sales = filtered_data.groupby('product')['sales'].sum().reset_index()
    product_fig = px.bar(
        product_sales, 
        x='product', 
        y='sales',
        title='Total Sales by Product'
    )
    product_fig.update_layout(height=400)
    
    # Sales by region
    region_sales = filtered_data.groupby('region')['sales'].sum().reset_index()
    region_fig = px.pie(
        region_sales, 
        values='sales', 
        names='region',
        title='Sales Distribution by Region'
    )
    region_fig.update_layout(height=400)
    
    # Heatmap
    heatmap_data = filtered_data.groupby(['product', 'region'])['sales'].sum().unstack(fill_value=0)
    heatmap_fig = px.imshow(
        heatmap_data,
        title='Sales Heatmap: Product vs Region',
        aspect='auto'
    )
    heatmap_fig.update_layout(height=400)
    
    return time_series_fig, product_fig, region_fig, heatmap_fig



# Run the app
if __name__ == '__main__':

    app.run_server(debug=True, host='0.0.0.0', port=8000)
