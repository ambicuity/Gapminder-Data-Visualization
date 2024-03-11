from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# Initialize Dash app
app = Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("Gapminder Data Visualization"),
    html.Div([
        dcc.Graph(id='scatter-chart'),
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='line-chart'),
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            step=None,
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
        ),
        dcc.Dropdown(
            id='continent-dropdown',
            options=[{'label': i, 'value': i} for i in df['continent'].unique()],
            value='Asia'
        ),
        dcc.Dropdown(
            id='scatter-x-variable',
            options=[{'label': i, 'value': i} for i in df.select_dtypes(include=['float64', 'int64']).columns],
            value='gdpPercap'
        ),
        dcc.Dropdown(
            id='scatter-y-variable',
            options=[{'label': i, 'value': i} for i in df.select_dtypes(include=['float64', 'int64']).columns],
            value='lifeExp'
        ),
        dcc.Dropdown(
            id='bar-variable',
            options=[{'label': i, 'value': i} for i in df.select_dtypes(include=['float64', 'int64']).columns],
            value='pop'
        ),
        dcc.Dropdown(
            id='color-variable',
            options=[{'label': i, 'value': i} for i in df.select_dtypes(include=['object']).columns],
            value='continent'
        ),
        dcc.Input(
            id='country-filter',
            type='text',
            value=''
        ),
        dcc.Checklist(
            id='population-toggle',
            options=[{'label': 'Percentage', 'value': 'Percentage'}],
            value=[]
        )
    ], style={'margin': '20px auto', 'width': '80%'}),
])

# Define callback to update scatter plot
@app.callback(
    Output('scatter-chart', 'figure'),
    [Input('year-slider', 'value'),
     Input('scatter-x-variable', 'value'),
     Input('scatter-y-variable', 'value'),
     Input('color-variable', 'value'),
     Input('country-filter', 'value')])
def update_scatter_chart(selected_year, x_variable, y_variable, color_variable, country_filter):
    filtered_df = df[df.year == selected_year]
    filtered_df = filtered_df[filtered_df['country'].str.contains(country_filter)]

    fig = px.scatter(filtered_df, x=x_variable, y=y_variable,
                     size="pop", color=color_variable, hover_name="country",
                     size_max=55)

    fig.update_layout(
        title=f"Scatter Plot ({selected_year})",
        xaxis_title=x_variable,
        yaxis_title=y_variable
    )

    return fig

# Define callback to update bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('year-slider', 'value'),
     Input('bar-variable', 'value'),
     Input('color-variable', 'value'),
     Input('population-toggle', 'value')])
def update_bar_chart(selected_year, bar_variable, color_variable, population_toggle):
    filtered_df = df[df.year == selected_year]
    if 'Percentage' in population_toggle:
        total_pop = filtered_df['pop'].sum()
        filtered_df['pop'] = filtered_df['pop'] / total_pop * 100
    bar_fig = px.bar(filtered_df, x="continent", y=bar_variable, color=color_variable, 
                     hover_name="country", title=f"Population Distribution by Continent ({selected_year})")
    bar_fig.update_layout(xaxis_title="Continent", yaxis_title=bar_variable)
    return bar_fig

# Define callback to update line chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input('year-slider', 'value'),
     Input('continent-dropdown', 'value')])
def update_line_chart(selected_year, selected_continent):
    filtered_df = df[df['year'] == selected_year]
    
    # Check if there is data available for the selected year
    if filtered_df.empty:
        return px.line(title=f"No Data Available for Year {selected_year}")
    
    # Check if there is data available for the selected continent in the selected year
    continent_data = filtered_df[filtered_df['continent'] == selected_continent]
    if continent_data.empty:
        return px.line(title=f"No Data Available for {selected_continent} in Year {selected_year}")
    
    line_fig = px.line(continent_data, x='year', y='gdpPercap', color='country', 
                       title=f"GDP per Capita Over Time in {selected_continent} ({selected_year})")
    line_fig.update_layout(xaxis_title="Year", yaxis_title="GDP per Capita (USD)")
    return line_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)