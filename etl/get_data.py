import yfinance as yf
import pandas as pd
import ta


def get_technical_indicators(ticker):
    """
    Fetch hourly stock data and compute technical indicators.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        pd.DataFrame: DataFrame containing stock data with calculated technical indicators.
    """
    # Download historical hourly data from Yahoo Finance starting from 2024-01-01
    data = yf.download(ticker, start="2024-01-01", interval="1h")

    # Check if data is retrieved
    if data.empty:
        print(f"No data retrieved for {ticker}.")
        return None

    # Drop any rows with missing values
    data.dropna(inplace=True)

    # Calculate technical indicators
    data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
    data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
    data['MACD'] = ta.trend.macd(data['Close'])
    data['MACD_Signal'] = ta.trend.macd_signal(data['Close'])
    data['MACD_Diff'] = ta.trend.macd_diff(data['Close'])
    data['Bollinger_High'] = ta.volatility.bollinger_hband(data['Close'], window=20)
    data['Bollinger_Low'] = ta.volatility.bollinger_lband(data['Close'], window=20)

    return data