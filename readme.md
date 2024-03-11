# Gapminder Data Visualization

This is a Dash application for visualizing Gapminder data. The application includes three types of charts: a scatter plot, a bar chart, and a line chart. The scatter plot shows the relationship between GDP per capita and life expectancy for different countries, with the size of each point representing the population and the color representing the continent. The bar chart shows the population distribution by continent, and the line chart shows the GDP per capita over time in a selected continent.

## Features

- Dropdown to select the continent for the line chart
- Dropdown to select the variable for the x-axis and y-axis of the scatter plot
- Dropdown to select the variable for the bar chart
- Dropdown to select the color variable for the scatter plot and bar chart
- Text input to filter countries based on their names
- Checkbox to toggle between absolute population and population as a percentage of the world population for the bar chart

## Installation

1. Clone this repository
2. Install the required packages: `pip install dash pandas plotly`
3. Run the app: `python app.py`

## Usage

Select the desired options from the dropdowns, input a country name to filter, and check the checkbox to toggle the population display. The charts will update automatically based on your selections.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MITs