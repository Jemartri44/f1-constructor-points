import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

# Read the DataFrame from CSV
df = pd.read_csv('data/results/final_results.csv')

# Define traditional colors for each constructor
team_colors = {
    "Alfa Romeo": "#9B0000",       # Deep red
    "AlphaTauri": "#2B4562",       # Dark blue
    "Alpine F1 Team": "#0090FF",   # Blue
    "Aston Martin": "#005C3F",     # Dark green
    "Caterham": "#32CD32",         # Lime green
    "Ferrari": "#DC0000",          # Ferrari red
    "Force India": "#F58025",      # Orange
    "HRT": "#708090",              # Slate gray
    "Haas F1 Team": "#A5ACAF",      # Silver-gray
    "Lotus": "#FFD700",            # Yellow (Team Lotus)
    "Lotus F1": "#1E90FF",         # Dodger blue
    "Manor Marussia": "#DAA520",   # Goldenrod
    "Marussia": "#800080",         # Purple
    "McLaren": "#FF8700",          # Papaya orange
    "Mercedes": "#00D2BE",         # Mercedes teal
    "Racing Point": "#FF66A3",     # Pinkish
    "Red Bull": "#1E41FF",         # Dark blue
    "Renault": "#FFF500",          # Bright yellow
    "Sauber": "#009FDB",           # Sauber blue
    "Toro Rosso": "#900000",       # Dark red
    "Virgin": "#6A0DAD",           # Purple
    "Williams": "#005AFF"          # Williams blue
}

app = dash.Dash(__name__)

# Get unique teams from the DataFrame and define year range
teams = sorted(df['team'].unique())
year_min = 2010
year_max = 2021

# App layout with enhanced styling
app.layout = html.Div([
    html.H1("F1 Constructor Points Dashboard", 
            style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif', 'color': '#333'}),
    
    # Year range slider card
    html.Div([
        html.Label("Select Year Range:", style={'fontWeight': 'bold'}),
        dcc.RangeSlider(
            id='year-slider',
            min=year_min,
            max=year_max,
            value=[year_min, year_max],
            marks={year: str(year) for year in range(year_min, year_max + 1)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True}
        )
    ], style={
        'backgroundColor': '#ffffff',
        'padding': '20px',
        'marginBottom': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    }),
    
    # Row container for constructor selection and graph
    html.Div([
        # Constructor selection card with checkboxes
        html.Div([
            html.Label("Select Constructors:", style={'fontWeight': 'bold'}),
            dcc.Checklist(
                id='team-checklist',
                options=[{'label': team, 'value': team} for team in teams],
                value=teams,  # All teams selected by default
                labelStyle={'display': 'block', 'padding': '5px 0'}
            )
        ], style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'width': '15%',
            'marginRight': '20px'
        }),
        
        # Graph card
        html.Div([
            dcc.Graph(id='points-graph', style={'height': '600px'})
        ], style={
            'flex': 1,
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        })
    ], style={'display': 'flex', 'flexWrap': 'wrap'})
    
], style={
    'maxWidth': '1400px',
    'width': '90%',
    'margin': '0 auto',
    'marginTop': '1%',
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f0f2f5',
    'padding': '20px'
})

@app.callback(
    Output('points-graph', 'figure'),
    [Input('team-checklist', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_teams, selected_years):
    # Filter the DataFrame based on the selected teams and years
    filtered_df = df[
        (df['team'].isin(selected_teams)) & 
        (df['year'] >= selected_years[0]) & 
        (df['year'] <= selected_years[1])
    ]
    
    fig = go.Figure()
    # New scaling factor: half of the previous (e.g., 2.5 instead of 5)
    scale_factor = 2.5
    
    # Create a trace for each team using their traditional color
    for team in selected_teams:
        team_df = filtered_df[filtered_df['team'] == team]
        if team_df.empty:
            continue
        
        fig.add_trace(go.Scatter(
            x=team_df['year'],
            y=team_df['mean'],
            mode='lines+markers',
            name=team,
            marker=dict(
                size=team_df['std'] * scale_factor,  # Marker size reflects the std deviation
                sizemode='diameter',
                opacity=0.7,
                line=dict(width=2),
                color=team_colors.get(team, '#000000')  # Use team color; default to black if not found
            ),
            hovertemplate='<b>%{text}</b><br><br>' +
                        'Year: %{x}<br>' +
                        'Mean Points: %{y:.2f}<br>' +
                        'Std Deviation: %{customdata:.2f}<br>' +
                        '<extra></extra>',
            text=team_df['team'],
            customdata=team_df['std']  # Pass std as custom data for the hover
        ))
    
    fig.update_layout(
        title="F1 Constructor Points: Average Points per Race with Std. Deviation",
        xaxis_title="Year",
        yaxis_title="Average Points per Race",
        xaxis=dict(dtick=1),
        template="plotly_white"
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
