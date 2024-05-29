import pandas as pd
import dash
from dash import Dash, html, dash_table, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

dash.register_page(__name__, path='/analysis_summary', name="📋Analysis Summary")

# Define the layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Investigating a Drop in User Engagement"), className="text-center my-4")
    ]),

    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H3("Situation", className="card-title"),
                html.P(
                    "Since August 4, 2014, WAU has decreased by 12%. We need to identify the causes of the decrease in WAU.",
                    className="card-text",
                    style={'fontSize': '18px', 'lineHeight': '2.0', 'textAlign': 'justify'}
                )
            ])
        ), width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H3("📊Analysis Summary", className="card-title"),
                html.Ul([
                    html.Li(
                        "Compared to the previous week, new sign-ups and new active users decreased by 14.71% and 19.23%, respectively. However, they have since recovered to the same level and slightly increased.",
                        style={'fontSize': '18px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "Although it is a typical pattern in the retention chart for active users to decrease over time from the point of sign-up, there was a noticeable drop in login engagement among users who signed up more than 10 weeks prior during the week of August 4, 2014.",
                        style={'fontSize': '18px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "WAU on phones and tablets decreased by 16.5% and 30.8%, respectively, compared to the previous week. There is a high likelihood that the issue is with the mobile app.",
                        style={'fontSize': '18px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "The number of link clicks in the weekly digest email and the proportion of users who clicked a link within 5 minutes of receiving the email both decreased compared to the previous week. We need to identify any issues related to the links in the digest email, such as the links themselves or the phrases encouraging clicks.",
                        style={'fontSize': '18px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    )
                ], style={'paddingLeft': '20px'})
            ])
        ), width=12)
    ], className="mb-4"), 

    dbc.Col(
    dbc.Card(
        dbc.CardBody([
            html.P(
                html.A(
                    "Data Source Link",
                    href="https://mode.com/sql-tutorial/a-drop-in-user-engagement",
                    target="_blank"  # This opens the link in a new tab
                ),
                className="card-text",
                style={'fontSize': '18px', 'lineHeight': '2.0', 'textAlign': 'justify'}
            ),

                html.P(
                    html.A(
                        "Git Link",
                        href="https://github.com/jongbokhi/yammer_project",
                        target="_blank"  # This opens the link in a new tab
                    ),
                    className="card-text",
                    style={'fontSize': '18px', 'lineHeight': '2.0', 'textAlign': 'justify'}
            )
        ])
    ),
    width=12
)
], fluid=True)

