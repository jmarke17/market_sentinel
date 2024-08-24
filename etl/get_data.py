import yfinance as yf
import pandas as pd
import ta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


import yfinance as yf
import pandas as pd
import ta
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_fundamental_data(ticker):
    """
    Retrieve and return fundamental data for a given stock ticker.
    Args:
        ticker (str): The stock ticker symbol.
    Returns:
        dict: A dictionary with fundamental data.
    """
    logging.info(f"Fetching fundamental data for {ticker}")

    stock = yf.Ticker(ticker)
    info = stock.info

    # Format the dividend yield as a percentage
    dividend_rate = info.get('dividendRate', 'N/A')
    dividend_yield = info.get('dividendYield', None)
    if dividend_yield is not None:
        dividend_yield_percentage = f"{dividend_yield * 100:.2f} %"
    else:
        dividend_yield_percentage = 'N/A'

    # Format the Ex-Dividend Date from timestamp to YYYY-MM-DD
    ex_dividend_timestamp = info.get('exDividendDate', None)
    if ex_dividend_timestamp is not None:
        ex_dividend_date = datetime.utcfromtimestamp(ex_dividend_timestamp).strftime('%Y-%m-%d')
    else:
        ex_dividend_date = 'N/A'

    # Collecting the relevant fundamental data
    data = {
        'Previous Close': info.get('previousClose', 'N/A'),
        'Open': info.get('open', 'N/A'),
        'Bid': info.get('bid', 'N/A'),
        'Ask': info.get('ask', 'N/A'),
        'Day Range': f"{info.get('dayLow', 'N/A')} - {info.get('dayHigh', 'N/A')}",
        '52 Week Range': f"{info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}",
        'Volume': info.get('volume', 'N/A'),
        'Avg. Volume': info.get('averageVolume', 'N/A'),
        'Market Cap': info.get('marketCap', 'N/A'),
        'Beta (5Y Monthly)': info.get('beta', 'N/A'),
        'PE Ratio (TTM)': info.get('trailingPE', 'N/A'),
        'EPS (TTM)': info.get('trailingEps', 'N/A'),
        'Earnings Date': info.get('earningsDate', 'N/A'),
        'Forward Dividend & Yield': f"{dividend_rate} ({dividend_yield_percentage})",
        'Ex-Dividend Date': ex_dividend_date,
        '1y Target Est': info.get('targetMeanPrice', 'N/A'),
    }

    logging.info(f"Fundamental data for {ticker}: {data}")
    return data



def get_technical_indicators(ticker):
    """
    Fetch hourly stock data and compute technical indicators.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        pd.DataFrame: DataFrame containing stock data with calculated technical indicators.
    """
    logging.info(f"Fetching technical data for {ticker}")

    # Download historical hourly data from Yahoo Finance starting from 2024-01-01
    data = yf.download(ticker, start="2024-01-01", interval="1h")

    # Check if data is retrieved
    if data.empty:
        logging.warning(f"No data retrieved for {ticker}.")
        return None

    # Drop any rows with missing values
    data.dropna(inplace=True)
    logging.info(f"Data for {ticker} retrieved successfully with {len(data)} rows.")

    # Calculate technical indicators
    data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
    data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
    data['MACD'] = ta.trend.macd(data['Close'])
    data['MACD_Signal'] = ta.trend.macd_signal(data['Close'])
    data['MACD_Diff'] = ta.trend.macd_diff(data['Close'])
    data['Bollinger_High'] = ta.volatility.bollinger_hband(data['Close'], window=20)
    data['Bollinger_Low'] = ta.volatility.bollinger_lband(data['Close'], window=20)

    logging.info(f"Technical indicators calculated for {ticker}")

    return data
