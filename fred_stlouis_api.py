import requests
import os 
from dotenv import load_dotenv
import datetime
import matplotlib.pyplot as plt


def get_series_data(series_id, start_date=None, end_date= None, frequency = None):

    """
    Fetches data for a specific series from the FRED API.

    Parameters:
        series_id (str): The FRED series ID you want to fetch data for.
        start_date (str, optional): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str, optional): The end date for the data in 'YYYY-MM-DD' format.
        frequency (str, optional): This specifies the interval for which a user wants the data. 

    Returns:
        dict: The JSON response from the FRED API parsed into a Python dictionary.
    """
    # Set default dates if not provided
    if start_date is None:
        start_date = '2000-01-01'  # Default start date
    if end_date is None:
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')  # Default end date is today
    if frequency is None:
        frequency = 'q'

    request_url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': frequency
    }
    

    try:
        response = requests.get(request_url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        observations = data['observations']
        plot_series(observations,series_id)
        return data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")  # Python 3.6
    except Exception as err:
        print(f"An error occurred: {err}")


def plot_series(observations,series_id):
    # Initializing lists to hold the values I need for the visuals
    dates = []
    values = []

    # Loop through observations to plot everything
    for obs in observations:
        date_str = obs['date']
        value_str = obs['value']

        ## Convert the string to a datetime object
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError as e:
            print(f"Date conversion error: {e}")
            continue 

            # Handle missing values represented as '.'
        if value_str == '.' or value_str == '':
            # Skip missing or empty values
            continue
        else:
            try:
                value = float(value_str)
            except ValueError as e:
                print(f"Value conversion error at date {date_str}: {e}")
                continue  # Skip this observation if value conversion fails

        # Append to the lists
        dates.append(date)
        values.append(value)

        date_start = dates[0].strftime('%m/%d/%Y')
        date_end = dates[-1].strftime('%m/%d/%Y')

    # Check if data lists are not empty
    if not dates or not values:
        print("No data available to plot.")
    else:
        # Now, create the line chart
        plt.figure(figsize=(10, 6))
        plt.plot(dates, values, marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title('Line Chart of {}: {} - {} from FRED Data'.format(series_id,date_start,date_end))
        plt.grid(True)
        
        # Format the x-axis to show dates nicely
        plt.gcf().autofmt_xdate()
        
        plt.show()

load_dotenv('keys.env')

api_key = os.getenv('fred_api_key')
if api_key is None:
    raise ValueError("API key not found. Please check your keys.env file.")

data = get_series_data('GDP','2015-01-01','2024-09-01','a')

