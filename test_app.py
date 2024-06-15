import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import pytest

# The app code
def create_app():
    # Load your data
    df = pd.read_csv('sales_data.csv')

    # Initialize the Dash app
    app = dash.Dash(__name__)

    # Define the layout of the app
    app.layout = html.Div([
        html.H1('Sales Data Visualizer', className='header'),
        dcc.RadioItems(
            id='region-selector',
            options=[
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'},
                {'label': 'All', 'value': 'all'}
            ],
            value='all',
            className='radio-buttons'
        ),
        dcc.Graph(id='sales-line-chart', className='line-chart')
    ], className='container')

    # Create a callback to update the graph based on the selected region
    @app.callback(
        Output('sales-line-chart', 'figure'),
        [Input('region-selector', 'value')]
    )
    def update_graph(selected_region):
        if selected_region == 'all':
            filtered_df = df
        else:
            filtered_df = df[df['region'] == selected_region]

        fig = px.line(filtered_df, x='date', y='sales', title=f'Sales in {selected_region.capitalize()} Region')
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Sales'
        )
        return fig

    return app

# Test suite
@pytest.fixture
def dash_duo(dash_duo):
    app = create_app()
    dash_duo.start_server(app)
    return dash_duo

def test_header_is_present(dash_duo):
    dash_duo.wait_for_text_to_equal('h1.header', 'Sales Data Visualizer', timeout=10)
    assert dash_duo.find_element('h1.header')

def test_visualization_is_present(dash_duo):
    dash_duo.wait_for_element_by_id('sales-line-chart', timeout=10)
    assert dash_duo.find_element('#sales-line-chart')

def test_region_picker_is_present(dash_duo):
    dash_duo.wait_for_element_by_id('region-selector', timeout=10)
    assert dash_duo.find_element('#region-selector')
