import dash
from dash import Dash, html, dash_table, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


# Initialize the app
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])


# Desired order of pages
desired_order = [
    '📋Analysis Summary',
    "🔎Situation",  
    "1️⃣Weekely Active User",
    "2️⃣User Cohort Analysis",
    "3️⃣User Device WAU",
    "4️⃣Email Action"
]

# Define the sidebar layout
sidebar = dbc.Col(
    [
        html.Br(),
        html.P('', className="text-dark text-center fw-bold fs-4"),
        html.Div(
            children=[
                dcc.Link(page['name'], href=page["relative_path"], className="btn btn-dark m-2 fs-5 d-block")
                for page_name in desired_order
                for page in dash.page_registry.values()
                if page['name'] == page_name
            ]
        )
    ],
    width=3,  # Width of the sidebar column
    className="bg-light"
)

# Define the main content layout
content = dbc.Col(
    dash.page_container,
    width=9,  # Width of the main content column
    className="p-4"
)

# Define the overall layout
app.layout = dbc.Container(
    dbc.Row([sidebar, content]),
    fluid=True
)

if __name__ == '__main__':
    app.run_server(debug=True)