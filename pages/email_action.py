import pandas as pd
import dash
from dash import Dash, html, dash_table, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import seaborn as sns


dash.register_page(__name__, path='/email_action', name="4️⃣Email Action")

# Read the data
email_action = pd.read_csv('email_action.csv')

open_ct_rate = pd.read_csv('open_ct_rate.csv')

email_op_rate = pd.DataFrame()
email_op_rate['weekly_open_rate(%)'] = round(open_ct_rate['weekly_digest_email_open']/open_ct_rate['weekly_digest_email'], 2)*100
email_op_rate['weekly_click_rate(%)'] = round(open_ct_rate['weekly_digest_email_click_through']/open_ct_rate['weekly_digest_email_open'], 2)*100
email_op_rate['retain_open_rate(%)'] = round(open_ct_rate['retain_opens']/open_ct_rate['retain_emails'], 2)*100
email_op_rate['retain_click_rate(%)'] = round(open_ct_rate['retain_ctr']/open_ct_rate['retain_opens'], 2)*100
email_op_rate.insert(0, 'week', open_ct_rate['week'])
email_op_rate.fillna(0)

#직전 주 대비 증감(Week On Week :WoW)

# Calculate Week On Week  change
email_pct_change_df = round(email_action[['email_clickthroughs']].pct_change()*100, 2)

email_action['email_clickthroughs_WoW(%)'] = email_pct_change_df
email_action.fillna(0)


def email_action_line_plot():
    fig = px.line(email_action, x='week', y=['email_clickthroughs_WoW(%)'])
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified", title="Email clickthroughs WoW", xaxis_title="Week", yaxis_title="%")
    
    return fig

def email_op_rate_line_plot():
    fig = px.line(email_op_rate, x='week', y=email_op_rate.columns)
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified", title="Email Open Rate", xaxis_title="Week", yaxis_title="%")
    
    return fig

# Create the figure
fig_email_action = email_action_line_plot()
fig_email_op_rate = email_op_rate_line_plot()


# Define the navigation panel
sidebar = html.Div(
    [
        html.H4("Contents", className="display-6", style={'fontSize': '23px'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Email Logs Analysis", href="#analysis1", external_link=True),
                dbc.NavLink("Clickthrough WoW Graph", href="#graph1", external_link=True),
                dbc.NavLink("Email Open Rate Analysis", href="#analysis2", external_link=True),
                dbc.NavLink("Email Open Rate Graph", href="#graph2", external_link=True),
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
        'padding': '2rem',
        'background-color': '#f8f9fa',
        'border-left': '10px solid #dee2e6',
        'z-index': '1000'  # Ensure the sidebar is above other elements
    },
)






# Define the layout
layout = html.Div([ 
    sidebar,
    html.Div(dbc.Container([


    dbc.Row([
        dbc.Col(html.H2("Email Action Analysis"), className="text-center my-4")
    ]),

    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.Ul([
                    html.H4("How does user engagement occur❓", className="text-left my-4")
                ], style={'paddingLeft': '18px'})
            ])
        ), width=12)
    ], className="mb-4"), 



    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.Ul([
                    html.H4("📊 Email Logs Analysis", id ="analysis1", className="text-left my-4"),
                    html.Li(
                        "The number of link clicks within emails (email clickthrough) decreased by 31.75% compared to the previous week on August 4.",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    )
                ], style={'paddingLeft': '20px'})
            ])
        ), width=12)
    ], className="mb-4"), 



    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                data=email_action.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in email_action.columns],
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
                html.Button('Show SQL Code', id='show-sql-button', n_clicks=0, className='btn btn-primary mt-2'),
                width=12
            )
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='sql-code'), width=12)
        ]),


      dbc.Row([
        dbc.Col(html.H4("Clickthrough WoW Graph", id ="graph1"), className="text-left my-4")], className="mb-4"), 

    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig_email_action),
            width=12
        )
    ]),


    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.Ul([
                    html.H4("📊 Email Open Rate Analysis", id ="analysis2", className="text-left my-4"),
                    html.Li(
                        "The proportion of users clicking links within the weekly digest email within 5 minutes of receiving it dropped sharply from 38% the week before August 4 to 23% after August 4.",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    )
                ], style={'paddingLeft': '20px'})
            ])
        ), width=12)
    ], className="mb-4"), 

    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                data=email_op_rate.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in email_op_rate.columns],
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
                html.Button('Show SQL Code', id='show-sql-button2', n_clicks=0, className='btn btn-primary mt-2'),
                width=12
            )
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='sql-code2'), width=12)
        ]),

    dbc.Row([
            dbc.Col(
                html.Button('Show Python Code', id='show-python-button', n_clicks=0, className='btn btn-primary mt-2'),
                width=12
            )
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='Python-code'), width=12)
        ]),

    dbc.Row([
        dbc.Col(html.H3("Email Open Rate Graph", id ="graph2"), className="text-left my-4")], className="mb-4"), 

    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig_email_op_rate),
            width=12
        )
    ]),


    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.Ul([
                    html.H4("Variable Information", id="Variable Information", className="text-left my-4"),
                    html.Li(
                        "weekly_open_rate: Open rate of weekly digest emails within 5 minutes of receipt",
                        style={'fontSize': '15px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "weekly_ctr: Click-through rate (CTR) of links within weekly digest emails within 5 minutes of receipt",
                        style={'fontSize': '15px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "retain_open_rate: Open rate of reengagement emails within 5 minutes of receipt",
                        style={'fontSize': '15px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'} 
                    
                    ),
                    html.Li(
                        "retain_ctr: Click-through rate (CTR) of links within reengagement emails within 5 minutes of receipt",
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
    Output('sql-code', 'children'),
    Input('show-sql-button', 'n_clicks'), 
)

def show_sql_code(n_clicks):
    if n_clicks % 2 == 1:
        sql_code = '''
            SELECT DATE_TRUNC('week', occurred_at) AS week,
            COUNT(CASE WHEN e.action = 'sent_weekly_digest' THEN e.user_id ELSE NULL END) AS weekly_emails,
            COUNT(CASE WHEN e.action = 'sent_reengagement_email' THEN e.user_id ELSE NULL END) AS reengagement_emails,
            COUNT(CASE WHEN e.action = 'email_open' THEN e.user_id ELSE NULL END) AS email_opens,
            COUNT(CASE WHEN e.action = 'email_clickthrough' THEN e.user_id ELSE NULL END) AS email_clickthroughs
            FROM tutorial.yammer_emails e
            GROUP BY week
            ORDER BY week;
        '''
        return [
            dbc.Row([
                dbc.Col(html.Pre(sql_code, style={'white-space': 'pre-wrap', 'word-break': 'break-all'}), width=12)
            ])
        ]
    else:
        return []
       

@callback(
    Output('sql-code2', 'children'),
    Input('show-sql-button2', 'n_clicks')
)

def show_sql_code2(n_clicks2):
    if n_clicks2 % 2 == 1:
        sql_code2 = '''
            SELECT 
                DATE_TRUNC('week', e1.occurred_at) AS week, 
                COUNT(CASE WHEN e1.action = 'sent_weekly_digest' THEN e1.user_id END) AS weekly_digest_email,
                COUNT(CASE WHEN e1.action = 'sent_weekly_digest' AND e2.action = 'email_open' THEN e1.user_id END) AS weekly_digest_email_open,
                COUNT(CASE WHEN e1.action = 'sent_weekly_digest' AND e3.action = 'email_clickthrough' THEN e1.user_id END) AS weekly_digest_email_click_through,
    
                COUNT(CASE WHEN e1.action = 'sent_reengagement_email' THEN e1.user_id ELSE NULL END) AS retain_emails,
                COUNT(CASE WHEN e1.action = 'sent_reengagement_email' THEN e2.user_id ELSE NULL END) AS retain_opens,
                COUNT(CASE WHEN e1.action = 'sent_reengagement_email' THEN e3.user_id ELSE NULL END) AS retain_ctr
    
            FROM 
                tutorial.yammer_emails e1
            LEFT JOIN 
                tutorial.yammer_emails e2 
            ON 
                e2.user_id = e1.user_id
            AND 
                e2.action = 'email_open'
            AND 
                e2.occurred_at BETWEEN e1.occurred_at AND e1.occurred_at + INTERVAL '5 MINUTE'
            LEFT JOIN 
                tutorial.yammer_emails e3 
            ON 
                e3.user_id = e1.user_id
            AND e
                3.action = 'email_clickthrough'
            AND 
                e3.occurred_at BETWEEN e1.occurred_at AND e1.occurred_at + INTERVAL '5 MINUTE'
            WHERE 
                e1.occurred_at BETWEEN '2014-06-01 00:00:00' AND '2014-08-31 23:59:59'
                AND e1.action IN ('sent_weekly_digest', 'sent_reengagement_email')
            GROUP BY 
                week
            ORDER BY 
                week;
        '''
        return [
            dbc.Row([
                dbc.Col(html.Pre(sql_code2, style={'white-space': 'pre-wrap', 'word-break': 'break-all'}), width=12)
            ])
        ]
    else:
        return []
    

@callback(
    Output('Python-code', 'children'),
    Input('show-python-button', 'n_clicks')
)

def show_python_code(n_clicks):
    if n_clicks % 2 == 1:
        python_code = '''
            email_op_rate = pd.DataFrame()
            email_op_rate['weekly_open_rate(%)'] = round(open_ct_rate['weekly_digest_email_open']/open_ct_rate['weekly_digest_email'], 2)*100
            email_op_rate['weekly_click_rate(%)'] = round(open_ct_rate['weekly_digest_email_click_through']/open_ct_rate['weekly_digest_email_open'], 2)*100
            email_op_rate['retain_open_rate(%)'] = round(open_ct_rate['retain_opens']/open_ct_rate['retain_emails'], 2)*100
            email_op_rate['retain_click_rate(%)'] = round(open_ct_rate['retain_ctr']/open_ct_rate['retain_opens'], 2)*100
            email_op_rate.insert(0, 'week', open_ct_rate['week'])
            email_op_rate.fillna(0)
        '''
        return [
            dbc.Row([
                dbc.Col(html.Pre(python_code, style={'white-space': 'pre-wrap', 'word-break': 'break-all'}), width=12)
            ])
        ]
    else:
        return []
       
