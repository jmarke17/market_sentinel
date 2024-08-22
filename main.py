from etl.get_data import get_technical_indicators
from etl.plot_data import plot_technical_indicators

# Define the stock ticker symbol
ticker = 'O'

# Get the technical indicators
df = get_technical_indicators(ticker)

# If data is retrieved successfully, plot the indicators
if df is not None:
    plot_technical_indicators(df, ticker)
else:
    print("Failed to retrieve data or plot technical indicators.")
