import pandas as pd
import dash
from dash import Dash, html, dash_table, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px


dash.register_page(__name__, path='/analysis_new_client', name="1️⃣Weekely Active User")

# Read the data
new_client_df = pd.read_csv(r'yammer_project\alluser_Vs_activated.csv')
new_client_week_df = pd.read_csv(r'yammer_project\weekly_active_user_week.csv')
new_client_week_df['signup_users_WoW(%)'] = round(new_client_week_df['signup_users'].pct_change()*100, 2)
new_client_week_df['activated_users_WoW(%)'] = round(new_client_week_df['activated_users'].pct_change()*100, 2)
new_client_week_df.fillna(0)
# Define the function for the line plot

def day_line_plot():
    fig = px.line(new_client_df , x='signup_date', y=new_client_df.columns,
                  title = 'Signup users(Day)')
    fig.update_traces(mode='markers+lines', hovertemplate=None)
    fig.update_layout(hovermode='x unified')
    return fig

def week_line_plot():
    fig = px.line(new_client_week_df , x='signup_date', y=['signup_users','activated_users'], 
                  title = 'Signup users(Week)')
    fig.update_traces(mode='markers+lines', hovertemplate=None)
    fig.update_layout(hovermode='x unified')
    return fig

# Create the figure
fig_day = day_line_plot()
fig_week= week_line_plot()


# Define the navigation panel
sidebar = html.Div(
    [
        html.H4("Contents", className="display-6", style={'fontSize': '23px'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("New sign-ups(daily)", href="#new_sign_daily", external_link=True),
                dbc.NavLink("Analysis", href="#new_sign_analysis", external_link=True),
                dbc.NavLink("New sign-ups(weekly)", href="#new_sign_weekly", external_link=True),
        
            ],
            vertical=True,
            pills=True,
        ),
    ],
    
    style={
        'position': 'fixed',
        'top': '5%',  # Adjust as needed
        'right': '0',
        'width': '240px',
        'padding': '1rem',
        'background-color': 'rgba(248, 249, 250, 0.4)',
        'border-left': '1px solid #dee2e6',
        'z-index': '1000'  # Ensure the sidebar is above other elements
    },
)

# Define the layout
layout = html.Div([
    sidebar,
    dbc.Container([

        dbc.Row([
        dbc.Col(html.H2("Weekly Active User Analysis"), className="text-center my-4")
    ]),
 
    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.Ul([
                    html.Li(
                        "Possibility ==> Did the decrease in new sign-ups affect WAU ❓",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "✅ The decrease in new sign-ups can directly impact the decrease in the number of logged-in users, as new sign-up users are expected to log in after registration.",
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
                    html.H3("📊Analysis", id ='new_sign_analysis',className="card-title"),
                    html.Li(
                        "In the week of August 4, 2014, compared to the previous week, new sign-ups and new active users decreased by 14.71% and 19.23%, respectively.",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "Subsequently, both new sign-ups and new active users recovered to the previous level and slightly increased.",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    
                    )
                ], style={'paddingLeft': '20px'})
            ])
        ), width=12)
    ], className="mb-4"), 

    dbc.Row([
        dbc.Col(html.H4("New sign-ups(daily)", id ='new_sign_daily', className="text-left my-4"))
    ]),

    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                data=new_client_df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in new_client_df.columns],
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
                html.Button('Show SQL Code', id='show-sql-button_wau', n_clicks=0, className='btn btn-primary mt-2'),
                width=12
            )
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='sql-code_wau'), width=12)
        ]),



    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig_day),
            width=12
        )
    ]), 
    dbc.Row([
        dbc.Col(html.H4("New Sign-ups (Weekly)"), id = 'new_sign_weekly', className="text-left my-4")
    ]),


    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                data=new_client_week_df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in new_client_week_df.columns],
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
                html.Button('Show SQL Code', id='show-sql-button_wau_week', n_clicks=0, className='btn btn-primary mt-2'),
                width=12
            )
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='sql-code_wau_week'), width=12)
        ]),


    dbc.Row([
            dbc.Col(
                html.Button('Show Python Code', id='show-python-button_wau_week', n_clicks=0, className='btn btn-primary mt-2'),
                width=12
            )
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='python-code_wau_week'), width=12)
        ]),




    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig_week),
            width=12
        )
    ]), 

], fluid=True)

])


# Show SQL code when button is clicked
@callback(
    Output('sql-code_wau', 'children'),
    Input('show-sql-button_wau', 'n_clicks'), 
)

def show_sql_code(n_clicks):
    if n_clicks % 2 == 1:
        sql_code = '''
                    #per day
                    
                    SELECT 
                        DATE_TRUNC('day', created_at) AS signup_date,
                        COUNT(user_id) AS signup_users,
                        COUNT(CASE WHEN activated_at IS NOT NULL THEN user_id ELSE NULL END) AS activated_users
                    FROM 
                        tutorial.yammer_users
                    WHERE 
                        created_at BETWEEN '2014-06-01 00:00:00' AND '2014-08-31 23:59:59'
                    GROUP BY 
                        signup_date;
                    '''
        return [
            dbc.Row([
                dbc.Col(html.Pre(sql_code, style={'white-space': 'pre-wrap', 'word-break': 'break-all'}), width=12)
            ])
        ]
    else:
        return []
    

@callback(
    Output('sql-code_wau_week', 'children'),
    Input('show-sql-button_wau_week', 'n_clicks'), 
)

def show_sql_code(n_clicks):
    if n_clicks % 2 == 1:
        sql_code = '''
                    #per week 
                    SELECT 
                        DATE_TRUNC('week', created_at) AS signup_date,
                        COUNT(user_id) AS signup_users,
                        COUNT(CASE WHEN activated_at IS NOT NULL THEN user_id ELSE NULL END) AS activated_users
                    FROM 
                        tutorial.yammer_users
                    WHERE 
                        created_at BETWEEN '2014-06-01 00:00:00' AND '2014-08-31 23:59:59'
                    GROUP BY 
                        signup_date;
                    '''
        return [
            dbc.Row([
                dbc.Col(html.Pre(sql_code, style={'white-space': 'pre-wrap', 'word-break': 'break-all'}), width=12)
            ])
        ]
    else:
        return []
    


@callback(
    Output('python-code_wau_week', 'children'),
    Input('show-python-button_wau_week', 'n_clicks'), 
)

def show_python_code(n_clicks):
    if n_clicks % 2 == 1:
        sql_code = '''
                    new_client_week_df['signup_users_WoW(%)'] = round(new_client_week_df['signup_users'].pct_change()*100, 2)

                    new_client_week_df['activated_users_WoW(%)'] = round(new_client_week_df['activated_users'].pct_change()*100, 2)

                    new_client_week_df.fillna(0)

                    '''
        return [
            dbc.Row([
                dbc.Col(html.Pre(sql_code, style={'white-space': 'pre-wrap', 'word-break': 'break-all'}), width=12)
            ])
        ]
    else:
        return []
