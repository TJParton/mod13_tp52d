import requests
import pygal
from pygal.style import DarkSolarizedStyle
from datetime import datetime

# Function to fetch stock data from Alpha Vantage
def get_stock_data(symbol, function, api_key, start_date, end_date):
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}&datatype=json'
    response = requests.get(url)
    
    # Check if the response is valid
    if response.status_code != 200:
        print(f"Error: Failed to retrieve data. HTTP Status code: {response.status_code}")
        return None
    
    data = response.json()
    
    # Debugging: Print the raw API response (optional)
    
    # Check if the response contains the expected key
    if 'Error Message' in data:
        print(f"Error: {data['Error Message']}")
        return None
    if not data:
        print("Error: No data received from API.")
        return None

    time_series_key = list(data.keys())[-1]  # Dynamic key name (daily, weekly, etc.)
    
    # Ensure the correct time series key exists
    if time_series_key not in data:
        print(f"Error: Time series data not found for {symbol}.")
        return None
    
    stock_data = data[time_series_key]
    
    # Filter data based on start_date and end_date
    filtered_data = {date: value for date, value in stock_data.items() if start_date <= date <= end_date}
    
    if not filtered_data:
        print(f"No data available for {symbol} in the specified date range ({start_date} to {end_date}).")
        first_available_date = list(stock_data.keys())[-1]
        print(f"Try extending your date range. Earliest available data is from {first_available_date}.")
        return None
    
    return filtered_data

# Function to generate the chart with Open, High, Low, and Close prices
def create_chart(data, title, chart_type):

    if chart_type == 1:
        chart_type = 'Line'
    elif chart_type == 2:
        chart_type = 'Bar'
    elif chart_type not in ['Line', 'Bar']:
        print("Invalid chart type!")
        return
    
    if chart_type == 'Line':
        chart = pygal.Line(style=DarkSolarizedStyle)
    elif chart_type == 'Bar':
        chart = pygal.Bar(style=DarkSolarizedStyle)
    else:
        print("Invalid chart type!")
        return

    chart.title = title
    chart.x_labels = list(data.keys())
    
    # Extracting Open, High, Low, and Close prices from the data
    open_prices = [float(info['1. open']) for info in data.values()]
    high_prices = [float(info['2. high']) for info in data.values()]
    low_prices = [float(info['3. low']) for info in data.values()]
    close_prices = [float(info['4. close']) for info in data.values()]

    # Adding data series to the chart
    chart.add('Open', open_prices)
    chart.add('High', high_prices)
    chart.add('Low', low_prices)
    chart.add('Close', close_prices)
    
    # Render the chart in the default web browser
    chart.render_in_browser()

# Function to validate date input
def validate_date_input(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print("Incorrect date format. Please use YYYY-MM-DD.")
        return None

# Main function to run the application
def run_application():
    api_key = '5EW2VPXRG7XF7PWK'

    # Get stock symbol from the user
    symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()

    # Ask for chart type
    chart_type = input("Enter the chart type (1)Line or (2)Bar: ")

    # Ask for the time series function
    print("Time series functions: (1)TIME_SERIES_DAILY, (2)TIME_SERIES_WEEKLY, (3)TIME_SERIES_MONTHLY")
    function = input("Enter the time series function: ").upper()

    # Ask for date range
    start_date = None
    while not start_date:
        start_date_input = input("Enter the beginning date (YYYY-MM-DD): ")
        start_date = validate_date_input(start_date_input)
    
    end_date = None
    while not end_date:
        end_date_input = input("Enter the end date (YYYY-MM-DD): ")
        end_date = validate_date_input(end_date_input)
        if end_date and end_date < start_date:
            print("End date cannot be before the start date.")
            end_date = None

    # Fetch and process stock data
    stock_data = get_stock_data(symbol, function, api_key, start_date_input, end_date_input)

    # Create and display chart
    if stock_data:
        create_chart(stock_data, f"{symbol} Stock Prices ({start_date_input} to {end_date_input})", chart_type)
    else:
        print(f"No data available for {symbol} in the specified date range.")

run_application()
