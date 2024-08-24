from etl.get_data import get_technical_indicators, get_fundamental_data
from etl.plot_data import plot_technical_indicators

# Define the stock ticker symbol
ticker = 'O'


df = get_technical_indicators(ticker)
fundamental_data = get_fundamental_data(ticker)

# If data is retrieved successfully, plot the indicators
if df is not None:
    plot_technical_indicators(df, ticker, fundamental_data)
else:
    print("Failed to retrieve data or plot technical indicators.")



