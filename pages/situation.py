import pandas as pd
import dash
from dash import Dash, html, dash_table, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px


dash.register_page(__name__, path='/situation', name="🔎 Situation")

# Read the data
weekly_active_user_df = pd.read_csv('weekly_active_user.csv')

# Define the function for the line plot
def line_plot(data):
    fig = px.line(data, x='week', y='weekly_active_user')
    fig.update_traces(mode='markers+lines', hovertemplate=None)
    fig.update_layout(hovermode='x unified')
    return fig

# Create the figure
fig = line_plot(weekly_active_user_df)

# Define the layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Decrease in Weekly Active Users(WAU)"), className="text-center my-4")
    ]),

    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.Ul([
                    html.Li(
                        "Decrease in WAU since August 4, 2014",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "The cause of the weekly active user decrease is unknown",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    ),
                    html.Li(
                        "Active users are counted as users who have logged in",
                        style={'fontSize': '20px', 'lineHeight': '2.0', 'textAlign': 'justify', 'marginBottom': '16px'}
                    )
                ], style={'paddingLeft': '20px'})
            ])
        ), width=12)
    ], className="mb-4"), 


    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                data=weekly_active_user_df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in weekly_active_user_df.columns],
                page_size=10,
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
                html.Button('Show SQL Code', id='show-sql-button_situation', n_clicks=0, className='btn btn-primary mt-2'),
                width=12
            )
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='sql-code_situation'), width=12)
        ]),

    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig),
            width=12
        )
    ]), 
    
], fluid=True)


# Show SQL code when button is clicked
@callback(
    Output('sql-code_situation', 'children'),
    Input('show-sql-button_situation', 'n_clicks'), 
)

def show_sql_code(n_clicks):
    if n_clicks % 2 == 1:
        sql_code = '''
                    SELECT 
                        DATE_TRUNC('week', e.occurred_at) AS week,
                        COUNT(DISTINCT user_id) as weekly_active_user
                    FROM 
                        tutorial.yammer_events e
                    WHERE 
                        occurred_at BETWEEN '2014-04-28 00:00:00' AND '2014-08-31 23:59:59'
                        AND e.event_type = 'engagement'
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
