import pandas as pd
import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output
from datetime import date
import datetime
import flask
import os

flask_app = flask.Flask(__name__)
app = dash.Dash(__name__, server=flask_app)
#app = dash.Dash()

# Loading data (source : https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data)
path_to_csv = './data/covid19.csv'
df = pd.read_csv(path_to_csv)
countries_list = list(set(df['countriesAndTerritories'][:]))

def format_countries(countries):
    my_options = []
    for c in countries:
        element = {'label' : c, 'value': c}
        my_options.append(element)

    return my_options

my_options = format_countries(countries_list)

app.layout = html.Div(children=[
    # Header
    html.H1('Covid19 statistics'),
    html.Br(),

    # Dropdown
    dcc.Dropdown(
        id='my_input',
        options=my_options,
        value='France'
    ),
    html.Br(),

    # Date range picker
    dcc.DatePickerRange(
        id='my-date-picker',
        min_date_allowed=date(2020, 3, 15),
        max_date_allowed=date.today(),
        initial_visible_month=date(2020, 3, 15),
        start_date=date(2020, 5, 1),
        end_date=date.today()
    ),

    # Graph
    html.Div(id='my_output', children=[])

])


@app.callback(
    Output(component_id='my_output', component_property='children'),
    [Input(component_id='my_input', component_property='value'),
     Input(component_id='my-date-picker', component_property='start_date'),
     Input(component_id='my-date-picker', component_property='end_date')]
)
def populate_fields(chosen_country, start_date, end_date):

    if start_date is not None and end_date is not None:

        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)

    # Filter database using our chosen country
    filtred_df = df[df['countriesAndTerritories'] == chosen_country]

    # Second filter using our chosen date range
    condition = [(datetime.datetime.strptime(i, '%d/%m/%Y').date() >= start_date and 
                datetime.datetime.strptime(i, '%d/%m/%Y').date() <= end_date) 
                for i in filtred_df['dateRep']]

    filtred_df = filtred_df[condition]
    
    # Getting the new cases and new deaths
    cases = filtred_df['cases']
    deaths = filtred_df['deaths']

    # Constructing a date range using start_date
    dates_list = [start_date + datetime.timedelta(days=x) for x in range(len(cases))]

    graph = dcc.Graph(
        id='covid',
        figure={
            'data' : [
                {'x' : dates_list, 'y':cases, 'type':'line', 'name':'New cases'},
                {'x' : dates_list, 'y':deaths, 'type':'line', 'name':'New deaths'}
            ]
        }
    )

    return graph
        


if __name__ == '__main__': 
    flask_app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
