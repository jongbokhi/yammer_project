import pandas as pd
import dash
from dash import Dash, html, dash_table, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import seaborn as sns


dash.register_page(__name__, path='/user_device_wau', name="3️⃣User Device WAU")

# Read the data
user_device_df = pd.read_csv('yammer_project\user_device.csv')

# Calculate Week On Week change
device_pct_change_df = round(user_device_df[['weekly_active_users', 'computer', 'phone', 'tablet']].pct_change() * 100, 2)

# Add the 'week' column back to the result
device_pct_change_df.insert(0, 'week', user_device_df['week'])
device_pct_change_df.fillna(0)

def device_line_plot():
    fig = px.line(user_device_df, x='week', y=user_device_df.columns)
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified", title="Weekly Engagement by Device Type", xaxis_title="Week", yaxis_title="Number of Users")
    return fig

def device_wow_line_plot():
    fig = px.line(device_pct_change_df, x='week', y=device_pct_change_df.columns)
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified", title="WoW", xaxis_title="Week", yaxis_title="%")
    return fig

# Create the figures
fig_device = device_line_plot()
fig_wow_device = device_wow_line_plot()

# Define the navigation panel
sidebar = html.Div(
    [
        html.H4("Contents", className="display-6", style={'fontSize': '23px'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Analysis", href="#analysis", external_link=True),
                dbc.NavLink("Weekly Engagement", href="#weekly-engagement", external_link=True),
                dbc.NavLink("Week On Week", href="#week-on-week", external_link=True),
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
    html.Div(
        dbc.Container([
           
        dbc.Row([
        dbc.Col(html.H2("WAU by Device"), className="text-center my-4", style={'fontSize': '23px'})
    ]),
            dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.Ul([
                    html.H3("📊Analysis", id="analysis", className="text-left my-4"),
                    html.Li(
                        "In the week starting August 4, 2014, WAU on phones and tablets decreased by 16.5% and 30.8%, respectively, compared to the previous week.",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "For computers, WAU in the week of August 4, 2014, decreased by 4% compared to the previous week; however, this appears to be seasonal (refer to data from the weeks of May 26 and June 30).",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "Nevertheless, computer traffic has not recovered and continues to decline, so further investigation is needed.",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'} 
                    
                    )
                ], style={'paddingLeft': '20px'})
            ])
        ), width=12)
    ], className="mb-4"), 

            
            dbc.Row([
                dbc.Col(
                    dash_table.DataTable(
                        data=user_device_df.to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in user_device_df.columns],
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
                    className="mb-4",
                    id="weekly-engagement"
                )
            ]),

            dbc.Row([
            dbc.Col(
                html.Button('Show SQL Code', id='show-sql-button_device', n_clicks=0, className='btn btn-primary mt-2'),
                width=12
            )
            ]),

            dbc.Row([
                dbc.Col(html.Div(id='sql-code_device'), width=12)
            ]),

            

            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=fig_device),
                    width=12
                )
            ]),
            dbc.Row([
                dbc.Col(html.H4("Week On Week (WoW)", id="week-on-week"), className="text-left my-4")
            ]),
            dbc.Row([
                dbc.Col(
                    dash_table.DataTable(
                        data=device_pct_change_df.to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in device_pct_change_df.columns],
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
                html.Button('Show Python Code', id='show-python-button_device_wow', n_clicks=0, className='btn btn-primary mt-2'),
                width=12
            )
            ]),

            dbc.Row([
                dbc.Col(html.Div(id='python-code_device_wow'), width=12)
            ]),


            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=fig_wow_device),
                    width=12
                )
            ])
        ], fluid=True),
        style={'margin-right': '220px'}
    )
])


# Show SQL code when button is clicked
@callback(
    Output('sql-code_device', 'children'),
    Input('show-sql-button_device', 'n_clicks'), 
)

def show_sql_code_device(n_clicks):
    if n_clicks % 2 == 1:
        sql_code = '''
                SELECT 
                    DATE_TRUNC('week', occurred_at) AS week,
                    COUNT(DISTINCT e.user_id) AS weekly_active_users,
                    COUNT(DISTINCT CASE WHEN e.device IN ('macbook pro','lenovo thinkpad','macbook air','dell inspiron notebook',
                                                            'asus chromebook','dell inspiron desktop','acer aspire notebook',
                                                            'hp pavilion desktop','acer aspire desktop','mac mini')
                                    THEN e.user_id ELSE NULL END) AS computer,
                    COUNT(DISTINCT CASE WHEN e.device IN ('iphone 5','samsung galaxy s4','nexus 5','iphone 5s','iphone 4s',
                                                            'nokia lumia 635','htc one','samsung galaxy note','amazon fire phone') 
                                    THEN e.user_id ELSE NULL END) AS phone,
                    COUNT(DISTINCT CASE WHEN e.device IN ('ipad air','nexus 7','ipad mini','nexus 10','kindle fire','windows surface',
                                                            'samsumg galaxy tablet') THEN e.user_id ELSE NULL END) AS tablet
                FROM tutorial.yammer_events e
                WHERE e.event_type = 'engagement' 
                        AND occurred_at BETWEEN '2014-04-28 00:00:00' AND '2014-08-31 23:59:59'
                        AND e.event_name = 'login'
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
    Output('python-code_device_wow', 'children'),
    Input('show-python-button_device_wow', 'n_clicks'), 
)

def show_python_code_device(n_clicks):
    if n_clicks % 2 == 1:
        python_code = '''
                
                    device_pct_change_df = round(user_device[['weekly_active_users', 'computer', 'phone', 'tablet']].pct_change()*100, 2)
                    
                    device_pct_change_df.insert(0, 'week', user_device['week'])

                    device_pct_change_df.fillna(0)
           
                '''
        return [
            dbc.Row([
                dbc.Col(html.Pre(python_code, style={'white-space': 'pre-wrap', 'word-break': 'break-all'}), width=12)
            ])
        ]
    else:
        return []
