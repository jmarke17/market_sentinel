import pandas as pd

def get_sp500_tickers():
    """
    Retrieve the list of S&P 500 tickers from Wikipedia.

    Returns:
        list: A list of ticker symbols in the S&P 500.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url)
    sp500_table = table[0]
    tickers = sp500_table['Symbol'].tolist()
    return tickers
