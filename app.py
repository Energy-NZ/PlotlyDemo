from dash import Dash, dcc, html, dash_table
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Load Apple stock data
df_apple = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

# Create line chart with range slider and selectors
fig_line = px.line(df_apple, x='Date', y='AAPL.High', title='Apple Stock Price - Daily High')

fig_line.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

# Apply theme to line chart
fig_line.update_layout(
    template="plotly_white",
    font=dict(family="Arial, sans-serif", size=12, color="#2c3e50"),
    title=dict(font=dict(size=20, color="#2c3e50"), x=0.5),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=60, r=60, t=80, b=60)
)

# Create pie chart data
df_pie = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
df_pie.loc[df_pie['pop'] < 2.e6, 'country'] = 'Other countries'  # Represent only large countries
fig_pie = px.pie(df_pie, values='pop', names='country', title='European Population Distribution (2007)')

# Apply theme to pie chart
fig_pie.update_layout(
    template="plotly_white",
    font=dict(family="Arial, sans-serif", size=12, color="#2c3e50"),
    title=dict(font=dict(size=20, color="#2c3e50"), x=0.5),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=60, r=60, t=80, b=60)
)

# Create table data - sample energy data for the client
df_table = pd.DataFrame({
    'Region': ['Auckland', 'Wellington', 'Christchurch', 'Hamilton', 'Tauranga', 'Dunedin'],
    'Energy Usage (GWh)': [2847.5, 1923.2, 1456.8, 892.1, 634.7, 521.3],
    'Renewable %': [78.2, 85.6, 82.1, 71.4, 69.8, 88.9],
    'Cost ($/MWh)': [89.50, 92.30, 87.20, 91.80, 94.10, 85.60],
    'Growth Rate': ['+3.2%', '+1.8%', '+2.1%', '+4.1%', '+2.9%', '+1.2%']
})

# Initialize Dash app with external stylesheet
app = Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
])
server = app.server  # for Render / Azure

# Custom CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .main-container {
                background: white;
                margin: 20px;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 30px 40px;
                margin: 0;
            }
            .content {
                padding: 30px 40px;
            }
            .chart-container {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }
            .flex-container {
                display: flex;
                gap: 30px;
                align-items: flex-start;
            }
            .table-container {
                flex: 1;
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }
            .pie-container {
                flex: 1;
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }
            .table-title {
                font-size: 20px;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 20px;
                text-align: center;
            }
            .separator {
                border: none;
                height: 2px;
                background: linear-gradient(90deg, transparent, #e9ecef, transparent);
                margin: 40px 0;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Layout with professional styling
app.layout = html.Div(className="main-container", children=[
    html.Div(className="header", children=[
        html.H1("Energy NZ Analytics Dashboard", 
                style={'margin': '0', 'fontSize': '32px', 'fontWeight': '600'})
    ]),
    html.Div(className="content", children=[
        html.Div(className="chart-container", children=[
            dcc.Graph(id='line-graph', figure=fig_line, 
                     config={'displayModeBar': True, 'displaylogo': False})
        ]),
        html.Hr(className="separator"),
        html.Div(className="flex-container", children=[
            html.Div(className="table-container", children=[
                html.Div("Regional Energy Summary", className="table-title"),
                dash_table.DataTable(
                    data=df_table.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df_table.columns],
                    style_cell={
                        'textAlign': 'center',
                        'fontFamily': 'Inter, Arial, sans-serif',
                        'fontSize': '14px',
                        'padding': '12px',
                        'border': '1px solid #e9ecef'
                    },
                    style_header={
                        'backgroundColor': '#2c3e50',
                        'color': 'white',
                        'fontWeight': '600',
                        'border': '1px solid #2c3e50'
                    },
                    style_data={
                        'backgroundColor': 'white',
                        'color': '#2c3e50'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f8f9fa'
                        }
                    ]
                )
            ]),
            html.Div(className="pie-container", children=[
                dcc.Graph(id='pie-graph', figure=fig_pie,
                         config={'displayModeBar': True, 'displaylogo': False})
            ])
        ])
    ])
])

# Run locally
if __name__ == "__main__":
    app.run(debug=True)