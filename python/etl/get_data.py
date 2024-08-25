import yfinance as yf
import pandas as pd
import ta
import logging
import re
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
    Fetch daily stock data and compute technical indicators.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        pd.DataFrame or None: DataFrame containing stock data with calculated technical indicators,
        or None if the data couldn't be retrieved.
    """
    logging.info(f"Fetching technical data for {ticker}")

    try:
        # Download historical daily data from Yahoo Finance for the last year
        data = yf.download(ticker, period="1y", interval="1d")

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

    except ValueError as e:
        logging.error(f"ValueError encountered for ticker {ticker}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error encountered for ticker {ticker}: {e}")
        return None


def calculate_score(df, fundamental_data):
    """
    Calculate a score based on technical indicators and fundamental data.

    Returns:
        int: A score from 0 to 100 indicating the buy potential of the stock.
    """
    score = 0

    # Technical Indicators (50%)
    rsi = df['RSI'].iloc[-1]
    macd = df['MACD'].iloc[-1]
    macd_signal = df['MACD_Signal'].iloc[-1]
    close_price = df['Close'].iloc[-1]
    bollinger_low = df['Bollinger_Low'].iloc[-1]

    # RSI based scoring
    if rsi < 30:
        score += 15  # Oversold, good buy signal
    elif rsi > 70:
        score -= 15  # Overbought, bad buy signal

    # MACD based scoring
    if macd > macd_signal:
        score += 20  # Bullish crossover, buy signal
    else:
        score -= 10  # Bearish crossover, sell signal

    # Bollinger Bands based scoring
    if close_price <= bollinger_low:
        score += 15  # Price near the lower band, potential buy signal

    # Fundamental Indicators (50%)
    dividend_yield = fundamental_data.get('Forward Dividend & Yield', '0').split(' ')[1]

    # Clean the dividend yield by removing any non-numeric characters except the decimal point
    dividend_yield = re.sub(r'[^\d.]', '', dividend_yield)

    if dividend_yield:
        dividend_yield = float(dividend_yield)
        if dividend_yield > 3:  # Assuming 3% is the market average
            score += 20  # High dividend yield

    pe_ratio = fundamental_data.get('PE Ratio (TTM)', 'N/A')
    if pe_ratio != 'N/A' and float(pe_ratio) < 15:  # Assuming 15 is the sector average
        score += 15  # Low PE ratio, good valuation

    beta = fundamental_data.get('Beta (5Y Monthly)', 'N/A')
    if beta != 'N/A' and float(beta) < 1:
        score += 15  # Low volatility

    # Ensure the score is within 0-100
    score = max(0, min(100, score))

    return score