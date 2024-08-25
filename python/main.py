from flask import Flask, render_template, request, redirect, url_for
from etl.get_data import get_technical_indicators, get_fundamental_data, calculate_score
from etl.plot_data import plot_technical_indicators
from etl.sp500_tickers import get_sp500_tickers  # Import the updated ticker retrieval function
import plotly.io as pio

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate-report', methods=['POST'])
def generate_report():
    ticker = request.form.get('ticker').upper()

    if not ticker:
        return redirect(url_for('home'))

    # Get data
    df = get_technical_indicators(ticker)
    fundamental_data = get_fundamental_data(ticker)

    if df is None:
        return f"<h3>Failed to retrieve data for {ticker}.</h3>"

    # Calculate SCORE
    score = calculate_score(df, fundamental_data)

    # Generate the Plotly figure as a div
    fig = plot_technical_indicators(df, ticker, fundamental_data, score)
    plot_div = pio.to_html(fig, full_html=False)

    # Render the report page
    return render_template('report.html', ticker=ticker, plot_div=plot_div, fundamental_data=fundamental_data)


@app.route('/find-good-score', methods=['GET'])
def find_good_score():
    tickers = get_sp500_tickers()

    best_ticker = None
    best_score = 0
    best_df = None
    best_fundamental_data = None

    for ticker in tickers:
        df = get_technical_indicators(ticker)
        if df is None:
            continue

        fundamental_data = get_fundamental_data(ticker)
        score = calculate_score(df, fundamental_data)

        # Keep track of the best score and corresponding ticker
        if score > best_score:
            best_ticker = ticker
            best_score = score
            best_df = df
            best_fundamental_data = fundamental_data

    if best_ticker:
        # Generate the Plotly figure as a div
        fig = plot_technical_indicators(best_df, best_ticker, best_fundamental_data, best_score)
        plot_div = pio.to_html(fig, full_html=False)

        # Render the report page for the best ticker
        return render_template('report.html', ticker=best_ticker, plot_div=plot_div,
                               fundamental_data=best_fundamental_data)

    return "<h3>No stock with a high enough score found in the S&P 500.</h3>"


if __name__ == '__main__':
    app.run(debug=True)


