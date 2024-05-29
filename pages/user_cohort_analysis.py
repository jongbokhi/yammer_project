import pandas as pd
import dash
from dash import Dash, html, dash_table, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px


dash.register_page(__name__, path='/user_cohort_analysis', name="2️⃣User Cohort Analysis")

# Read the data
user_cohort_df = pd.read_csv('User_cohort_analysis.csv')
user_cohort_df.drop(['Average age during week'], axis = 1, inplace = True)

def cohort_line_plot():
    fig = px.line(user_cohort_df, x='week', y=user_cohort_df.columns)
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified", title="User Cohort Analysis", xaxis_title="Week", yaxis_title="Number of Users")
    
    return fig


# Create the figure
fig_cohort = cohort_line_plot()


# Define the navigation panel
sidebar = html.Div(
    [
        html.H4("Contents", className="display-6", style={'fontSize': '23px'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Analysis", href="#analysis", external_link=True),
                dbc.NavLink("Visualization", href="#visualization", external_link=True),
                dbc.NavLink("Variable Information", href="#Variable Information", external_link=True),
        
            ],
            vertical=True,
            pills=True,
        ),
    ],
    
    style={
        'position': 'fixed',
        'top': '5%',  # Adjust as needed
        'right': '0',
        'width': '250px',
        'padding': '1rem',
        'background-color': 'rgba(248, 249, 250, 0.4)',
        'border-left': '1px solid #dee2e6',
        'z-index': '1000'  # Ensure the sidebar is above other elements
    },
)




# Define the layout
layout = html.Div([ 
    sidebar,
    html.Div(dbc.Container([

        dbc.Row([
        dbc.Col(html.H2("User Cohort Analysis"), className="text-center my-4")
    ]),

    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.Ul([
                    html.Li(
                        "Possibility ==> Wouldn't breaking down WAU by user cohorts help identify which groups of users are problematic based on their sign-up periods❓",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    )
                ], style={'paddingLeft': '20px'})
            ])
        ), width=12)
    ], className="mb-4"),


    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.Ul([
                    html.H3("📊Analysis", id="analysis", className="card-title"),
                    html.Li(
                        "It is a typical pattern in retention charts for the number of active users to decrease over time from the point of sign-up.",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "However, users who signed up more than 10 weeks ago show an exceptional drop in WAU during the week of August 4, 2014, which indicates an impact on WAU.",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "To compare whether user engagement is decreasing faster or slower, a baseline chart is needed to show how engagement decreases over time.",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'} 
                    
                    )
                ], style={'paddingLeft': '20px'})
            ])
        ), width=12)
    ], className="mb-4"), 



    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                data=user_cohort_df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in user_cohort_df.columns],
                page_size=18,
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'color': 'black',
                    'fontWeight': 'bold',
                    'textAlign': 'center'
                },
                style_cell={
                    'textAlign': 'center',
                    'padding': '5px',
                    'backgroundColor': 'rgb(250, 250, 250)',
                    'color': 'black'
                },
            ),
            width=12,
            className="mb-4"
        )
    ]),

    dbc.Row([
            dbc.Col(
                html.Button('Show SQL Code', id='show-sql-button_cohort', n_clicks=0, className='btn btn-primary mt-2'),
                width=12
            )
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='sql-code_cohort'), width=12)
        ]),


    dbc.Row([
        dbc.Col(html.H2("Visualization", id="visualization"), className="text-left my-4")
    ]),

    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig_cohort),
            width=12
        )
    ]), 

    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.Ul([
                    html.H4("Variable Information", id="Variable Information", className="text-left my-4"),
                    html.Li(
                        "Less than a week: Users who signed up within a week",
                        style={'fontSize': '15px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "n weeks: Users who signed up n weeks ago",
                        style={'fontSize': '15px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "10+ weeks: Users who signed up more than 10 weeks ago",
                        style={'fontSize': '15px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'} 
                    
                    )
                ], style={'paddingLeft': '20px'})
            ])
        ), width=12)
    ], className="mb-4"), 


   
], fluid=True),
style={'margin-right': '220px'}
    )
])

# Show SQL code when button is clicked
@callback(
    Output('sql-code_cohort', 'children'),
    Input('show-sql-button_cohort', 'n_clicks'), 
)

def show_sql_code_cohort(n_clicks):
    if n_clicks % 2 == 1:
        sql_code = '''
                SELECT 
                    DATE_TRUNC('week',z.occurred_at) AS "week",
                    AVG(z.age_at_event) AS "Average age during week",
                    COUNT(DISTINCT CASE WHEN z.user_age > 70 THEN z.user_id ELSE NULL END) AS "10+ weeks",
                    COUNT(DISTINCT CASE WHEN z.user_age < 70 AND z.user_age >= 63 THEN z.user_id ELSE NULL END) AS "9 weeks",
                    COUNT(DISTINCT CASE WHEN z.user_age < 63 AND z.user_age >= 56 THEN z.user_id ELSE NULL END) AS "8 weeks",
                    COUNT(DISTINCT CASE WHEN z.user_age < 56 AND z.user_age >= 49 THEN z.user_id ELSE NULL END) AS "7 weeks",
                    COUNT(DISTINCT CASE WHEN z.user_age < 49 AND z.user_age >= 42 THEN z.user_id ELSE NULL END) AS "6 weeks",
                    COUNT(DISTINCT CASE WHEN z.user_age < 42 AND z.user_age >= 35 THEN z.user_id ELSE NULL END) AS "5 weeks",
                    COUNT(DISTINCT CASE WHEN z.user_age < 35 AND z.user_age >= 28 THEN z.user_id ELSE NULL END) AS "4 weeks",
                    COUNT(DISTINCT CASE WHEN z.user_age < 28 AND z.user_age >= 21 THEN z.user_id ELSE NULL END) AS "3 weeks",
                    COUNT(DISTINCT CASE WHEN z.user_age < 21 AND z.user_age >= 14 THEN z.user_id ELSE NULL END) AS "2 weeks",
                    COUNT(DISTINCT CASE WHEN z.user_age < 14 AND z.user_age >= 7 THEN z.user_id ELSE NULL END) AS "1 week",
                    COUNT(DISTINCT CASE WHEN z.user_age < 7 THEN z.user_id ELSE NULL END) AS "Less than a week"
                FROM (
                        SELECT e.occurred_at,
                            u.user_id,
                            DATE_TRUNC('week',u.activated_at) AS activation_week,
                            EXTRACT('day' FROM e.occurred_at - u.activated_at) AS age_at_event,
                            EXTRACT('day' FROM '2014-09-01'::TIMESTAMP - u.activated_at) AS user_age
                        FROM tutorial.yammer_users u
                        JOIN tutorial.yammer_events e
                            ON e.user_id = u.user_id
                            AND e.event_type = 'engagement'
                            AND e.event_name = 'login'
                            AND e.occurred_at >= '2014-05-01'
                            AND e.occurred_at < '2014-09-01'
                        WHERE u.activated_at IS NOT NULL
                        ) z

                    GROUP BY week
                    ORDER BY week
                    LIMIT 100;
                    '''
        return [
            dbc.Row([
                dbc.Col(html.Pre(sql_code, style={'white-space': 'pre-wrap', 'word-break': 'break-all'}), width=12)
            ])
        ]
    else:
        return []
