import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import dash_daq as daq  # For interactive calendar component

# Sample data (replace with your real Instagram data)
df_followers_growth = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=30, freq='D'),
    'Followers': [100 + i * 5 for i in range(30)]
})

df_engagement = pd.DataFrame({
    'Post': ['Post 1', 'Post 2', 'Post 3', 'Post 4', 'Post 5'],
    'Likes': [120, 150, 90, 110, 95],
    'Comments': [15, 25, 10, 12, 8]
})

df_top_posts = pd.DataFrame({
    'Post': ['Post 1', 'Post 2', 'Post 3'],
    'Engagement Rate': [4.5, 5.0, 3.2],
    'Likes': [120, 150, 90],
    'Comments': [15, 25, 10]
})

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sidebar layout
sidebar = dbc.Col(
    [
        html.Img(src='https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png', style={'width': '100px', 'margin': '20px auto', 'display': 'block'}),
        html.H2("Dashboard", className="text-center", style={"color": "#E1306C"}),
        dbc.Nav(
            [
                dbc.NavLink("Analytics", href="/analytics", active="exact"),
                dbc.NavLink("Analysis", href="/analysis", active="exact"),
                dbc.NavLink("Content Generation", href="/content-generation", active="exact"),
                dbc.NavLink("Instagram Account", href="/instagram-account", active="exact"),
                dbc.NavLink("Tips", href="/tips", active="exact"),
                dbc.NavLink("Content Calendar", href="/content-calendar", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    width=3,
)

# Main content layout
content = dbc.Col(id="page-content", width=9)

# Main layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([sidebar, content])
])

# Callback to update content based on the selected link
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/analytics":
        return html.Div([
            html.H1("Instagram Analytics Dashboard", className="text-center mb-4", style={"color": "#E1306C"}),
            dbc.Row([
                dbc.Col(html.Div([
                    html.H3("Total Followers"),
                    html.H4(f"{df_followers_growth['Followers'].iloc[-1]}", style={"color": "#007bff"})
                ]), width=3),
                dbc.Col(html.Div([
                    html.H3("Engagement Rate"),
                    html.H4(f"{df_engagement['Likes'].sum() / df_engagement['Likes'].count():.2%}", style={"color": "#28a745"})
                ]), width=3),
                dbc.Col(html.Div([
                    html.H3("Average Likes/Post"),
                    html.H4(f"{df_engagement['Likes'].mean():.0f}", style={"color": "#dc3545"})
                ]), width=3),
                dbc.Col(html.Div([
                    html.H3("Average Comments/Post"),
                    html.H4(f"{df_engagement['Comments'].mean():.0f}", style={"color": "#ffc107"})
                ]), width=3),
            ], className="mb-5"),
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id='followers-growth',
                    figure=px.line(df_followers_growth, x='Date', y='Followers', title="Followers Growth").update_layout(plot_bgcolor='rgba(0,0,0,0)')
                ), width=12),
            ], className="mb-5"),
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id='engagement-metrics',
                    figure=px.bar(df_engagement, x='Post', y=['Likes', 'Comments'], barmode='group', title="Engagement Metrics").update_layout(plot_bgcolor='rgba(0,0,0,0)')
                ), width=12),
            ], className="mb-5"),
            dbc.Row([
                dbc.Col(html.Div([
                    html.H3("Top Performing Posts"),
                    dbc.Table.from_dataframe(df_top_posts, striped=True, bordered=True, hover=True)
                ]), width=12),
            ])
        ])
    elif pathname == "/analysis":
        return html.Div([
            html.H1("Analysis Page", className="text-center", style={"marginBottom": "20px", "color": "#E1306C"}),
            html.P("Here you can perform deeper analysis on your Instagram data.", className="text-center"),
            html.Div("This is where you'd implement data analysis based on your needs.", style={"textAlign": "center", "padding": "20px", "border": "1px solid #ccc"})
        ])
    elif pathname == "/content-generation":
        return html.Div([
            html.H1("Content Generation", className="text-center", style={"marginBottom": "20px", "color": "#E1306C"}),
            html.Div(id='chat-container', style={"border": "1px solid #ccc", "padding": "10px", "height": "400px", "overflowY": "scroll", "marginBottom": "10px"}),
            dcc.Input(id='chat-input', type='text', placeholder='Ask a question about Instagram...', style={"width": "80%", "display": "inline-block"}),
            html.Button('Send', id='chat-submit', n_clicks=0, style={"display": "inline-block", "backgroundColor": "#E1306C", "color": "white", "borderRadius": "5px", "padding": "5px 10px"}),
        ])
    elif pathname == "/instagram-account":
        return html.Div([
            html.H1("Instagram Account Linking", className="text-center", style={"marginBottom": "20px", "color": "#E1306C"}),
            dbc.Card(
                dbc.CardBody([
                    dbc.Input(id='instagram-username', type='text', placeholder='Enter Instagram Username', style={"marginBottom": "10px"}),
                    dbc.Input(id='instagram-password', type='password', placeholder='Enter Instagram Password', style={"marginBottom": "10px"}),
                    html.Button('Link Account', id='link-account', n_clicks=0, className="btn btn-primary", style={"marginBottom": "10px"}),
                    html.Div(id='account-details', style={"marginTop": "20px", "fontSize": "1.2em", "fontWeight": "bold"}),
                ]),
                style={"width": "50%", "margin": "0 auto", "padding": "20px", "border": "2px solid #E1306C", "borderRadius": "10px"}
            ),
        ])
    elif pathname == "/tips":
        return html.Div([
            html.H1("Tips to Increase Growth on Instagram", className="text-center", style={"marginBottom": "20px", "color": "#E1306C"}),
            html.Ul([
                html.Li("Post consistently and at optimal times."),
                html.Li("Engage with your audience by responding to comments."),
                html.Li("Use relevant hashtags to reach a broader audience."),
                html.Li("Collaborate with other users and brands."),
                html.Li("Utilize Instagram Stories to engage with followers."),
                html.Li("Run contests or giveaways to attract new followers."),
                html.Li("Create high-quality, visually appealing content."),
                html.Li("Leverage Instagram Reels for wider reach."),
                html.Li("Analyze your insights to understand what works."),
                html.Li("Share user-generated content to build community."),
                html.Li("Use a consistent theme and aesthetic."),
                html.Li("Add location tags to your posts."),
                html.Li("Use Instagram Ads for targeted reach."),
                html.Li("Network with influencers in your niche."),
                html.Li("Host live sessions to interact in real-time."),
                html.Li("Cross-promote your Instagram on other platforms."),
                html.Li("Keep up with Instagram trends and features."),
                html.Li("Encourage followers to turn on post notifications."),
                html.Li("Be authentic and showcase your brand's personality."),
                html.Li("Utilize analytics tools for better insights."),
                html.Li("Be patient and persistent in your growth strategy.")
            ])
        ])
    elif pathname == "/content-calendar":
        return html.Div([
            html.H1("Content Calendar", className="text-center", style={"marginBottom": "20px", "color": "#E1306C"}),
            dcc.DatePickerSingle(
                id='date-picker',
                date=pd.to_datetime('today'),
                style={'margin': '20px auto', 'display': 'block'}
            ),
            dbc.Input(id='calendar-note', type='text', placeholder='Add a note for this date', style={"marginBottom": "10px"}),
            html.Button('Save Note', id='save-note', n_clicks=0, style={"marginBottom": "10px"}),
            html.Div(id='calendar-notes', style={"marginTop": "20px", "fontSize": "1.2em", "fontWeight": "bold"}),
        ])
    else:
        return html.Div([html.H1("Welcome to the Dashboard", style={"color": "#E1306C", "textAlign": "center"})])  # Default landing page

# Callback to handle chat submission
@app.callback(
    Output('chat-container', 'children'),
    Input('chat-submit', 'n_clicks'),
    State('chat-input', 'value'),
    State('chat-container', 'children'),
    prevent_initial_call=True
)
def update_chat(n_clicks, value, existing_chats):
    if not value:
        raise dash.exceptions.PreventUpdate

    user_message = html.Div(f"User: {value}", style={"marginBottom": "5px", "fontWeight": "bold"})
    response = f"You asked: {value}"
    bot_response = html.Div(f"Bot: {response}", style={"marginBottom": "10px", "color": "#007bff"})

    return existing_chats + [user_message, bot_response]

# Callback to handle account linking
@app.callback(
    Output('account-details', 'children'),
    Input('link-account', 'n_clicks'),
    State('instagram-username', 'value'),
    State('instagram-password', 'value'),
    prevent_initial_call=True
)
def link_account(n_clicks, username, password):
    if not username or not password:
        return "Please enter both username and password."

    # Simulate account linking (you can replace this with actual linking logic)
    return f"Linked Account: {username}"

# Callback to save note in calendar
@app.callback(
    Output('calendar-notes', 'children'),
    Input('save-note', 'n_clicks'),
    State('date-picker', 'date'),
    State('calendar-note', 'value'),
    prevent_initial_call=True
)
def save_calendar_note(n_clicks, date, note):
    if not date or not note:
        return "Please select a date and enter a note."

    return f"Note for {date}: {note}"

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
