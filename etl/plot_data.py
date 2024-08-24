import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
import logging

def plot_technical_indicators(df, ticker, fundamental_data):
    """
    Generate an interactive HTML report with separate plots for Bollinger Bands, MACD, and RSI using Plotly,
    and include a table of fundamental data.

    Args:
        df (pd.DataFrame): DataFrame containing stock data and technical indicators.
        ticker (str): The stock ticker symbol.
        fundamental_data (dict): Dictionary containing the stock's fundamental data.
    """
    pio.templates.default = "plotly_dark"

    # Create subplots: 3 rows for Bollinger Bands, RSI, and MACD
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                        subplot_titles=("Bollinger Bands", "RSI", "MACD"))

    # Bollinger Bands plot
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price',
                             line=dict(color='white', width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['Bollinger_High'], mode='lines', name='Bollinger High',
                             line=dict(color='cyan', width=1, dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['Bollinger_Low'], mode='lines', name='Bollinger Low',
                             line=dict(color='cyan', width=1, dash='dash')), row=1, col=1)

    # RSI plot
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI',
                             line=dict(color='green', width=2)), row=2, col=1)
    fig.add_hline(y=70, line=dict(color="red", dash='dash'), annotation_text="Overbought", row=2, col=1)
    fig.add_hline(y=30, line=dict(color="blue", dash='dash'), annotation_text="Oversold", row=2, col=1)

    # MACD plot
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name='MACD',
                             line=dict(color='purple', width=2)), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], mode='lines', name='MACD Signal',
                             line=dict(color='orange', width=2, dash='dash')), row=3, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df['MACD_Diff'], name='MACD Diff',
                         marker_color='gray', opacity=0.5), row=3, col=1)

    # Update layout for the overall figure
    fig.update_layout(
        title=f"{ticker} - Technical Indicators",
        xaxis_title="Date",
        margin=dict(l=40, r=40, t=80, b=50),
        hovermode="x unified",
        template="plotly_dark",
        font=dict(family="Arial, sans-serif", size=12, color="white"),
        height=950
    )

    # Create an HTML table for fundamental data with black background and yellow text
    table_html = """
    <table border="1" style="width:70%; margin: 20px auto; font-family: Arial, sans-serif; background-color: black; color: yellow; border-collapse: collapse; text-align: left;">
        <caption style="font-size: 24px; font-weight: bold; color: yellow; margin-bottom: 10px;">Fundamental Data</caption>
        <tr style="background-color: #333;">
            <th style="padding: 8px; border: 1px solid #555;">Metric</th>
            <th style="padding: 8px; border: 1px solid #555;">Value</th>
        </tr>"""
    for key, value in fundamental_data.items():
        table_html += f"<tr><td style='padding: 8px; border: 1px solid #555;'>{key}</td><td style='padding: 8px; border: 1px solid #555;'>{value}</td></tr>"
    table_html += "</table><br>"

    # Save the plot as an HTML file with UTF-8 encoding
    with open(f"{ticker}_technical_indicators.html", "w", encoding="utf-8") as file:
        file.write(
            f"<!DOCTYPE html><html><head><title>{ticker} Technical and Fundamental Analysis</title></head><body style='background-color: black;'>")
        file.write(table_html)  # Add the fundamental data table
        file.write(fig.to_html(full_html=False))  # Add the technical indicators plot
        file.write("</body></html>")

    logging.info(f"Interactive HTML report saved as {ticker}_technical_indicators.html")

