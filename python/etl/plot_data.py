import plotly.graph_objs as go
from plotly.subplots import make_subplots

def plot_technical_indicators(df, ticker, fundamental_data, score):
    """
    Generate an interactive plot with technical indicators and a SCORE bar.
    """
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                        subplot_titles=("Bollinger Bands", "RSI", "MACD", "Buy Score"))

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

    # SCORE plot
    fig.add_trace(go.Bar(x=[score], y=["Buy Score"], orientation='h',
                         marker=dict(color='orange'),
                         width=[0.4], text=f"{score} / 100", textposition='outside'), row=4, col=1)

    # Adjust the x-axis range and ticks for the SCORE plot
    fig.update_xaxes(range=[0, 100], tickvals=[0, 50, 100], row=4, col=1)

    # Add annotation to show the score explicitly
    fig.add_annotation(x=score, y=-0.2, text=f"Score: {score} / 100",
                       showarrow=False, row=4, col=1,
                       font=dict(size=14, color='orange'), xanchor='center')

    # Update layout to ensure the x-axis is correctly displayed across all subplots
    fig.update_layout(
        title=f"{ticker} - Technical Indicators and Buy Score",
        xaxis_title="Date",
        xaxis=dict(showline=True, showgrid=True, tickangle=-45),
        margin=dict(l=40, r=40, t=80, b=50),
        hovermode="x unified",
        template="plotly_dark",
        font=dict(family="Arial, sans-serif", size=12, color="white"),
        height=1200
    )

    return fig


def plot_rolling_correlation(data, ticker1, ticker2, window=30):
    """
    Plot the rolling correlation between two assets using a specified window size.

    Args:
        data (pd.DataFrame): DataFrame containing the closing prices of the two assets.
        ticker1 (str): The first stock ticker symbol.
        ticker2 (str): The second stock ticker symbol.
        window (int): The window size for calculating the rolling correlation.
    """
    # Calculate the percentage change
    data[f'{ticker1}_Pct_Change'] = data[f'{ticker1}_Close'].pct_change() * 100
    data[f'{ticker2}_Pct_Change'] = data[f'{ticker2}_Close'].pct_change() * 100

    # Drop NaN values
    data = data.dropna()

    # Calculate rolling correlation
    data['Rolling_Corr'] = data[f'{ticker1}_Pct_Change'].rolling(window=window).corr(data[f'{ticker2}_Pct_Change'])

    # Plot the rolling correlation
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['Rolling_Corr'], mode='lines', name=f'Rolling Correlation ({window} days)'))

    # Update the layout of the figure
    fig.update_layout(
        title=f'Rolling Correlation ({window} days) between {ticker1} and {ticker2}',
        xaxis_title='Date',
        yaxis_title='Correlation',
        template='plotly_dark',
        height=600
    )

    return fig

def plot_scatter_pct_change(data, ticker1, ticker2):
    """
    Plot a scatter plot comparing the percentage change of two assets.

    Args:
        data (pd.DataFrame): DataFrame containing the closing prices of the two assets.
        ticker1 (str): The first stock ticker symbol.
        ticker2 (str): The second stock ticker symbol.
    """
    # Calculate the percentage change
    data[f'{ticker1}_Pct_Change'] = data[f'{ticker1}_Close'].pct_change() * 100
    data[f'{ticker2}_Pct_Change'] = data[f'{ticker2}_Close'].pct_change() * 100

    # Drop NaN values
    data = data.dropna()

    # Plot the scatter plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data[f'{ticker1}_Pct_Change'], y=data[f'{ticker2}_Pct_Change'], mode='markers',
                             name='Scatter Plot'))

    # Update the layout of the figure
    fig.update_layout(
        title=f'Scatter Plot of % Change: {ticker1} vs {ticker2}',
        xaxis_title=f'{ticker1} % Change',
        yaxis_title=f'{ticker2} % Change',
        template='plotly_dark',
        height=600
    )

    return fig

def plot_cumulative_returns(data, ticker1, ticker2):
    """
    Plot the cumulative returns of two assets.

    Args:
        data (pd.DataFrame): DataFrame containing the closing prices of the two assets.
        ticker1 (str): The first stock ticker symbol.
        ticker2 (str): The second stock ticker symbol.
    """
    # Calculate the percentage change
    data[f'{ticker1}_Pct_Change'] = data[f'{ticker1}_Close'].pct_change()
    data[f'{ticker2}_Pct_Change'] = data[f'{ticker2}_Close'].pct_change()

    # Drop NaN values
    data = data.dropna()

    # Calculate cumulative returns
    data[f'{ticker1}_Cumulative'] = (1 + data[f'{ticker1}_Pct_Change']).cumprod() - 1
    data[f'{ticker2}_Cumulative'] = (1 + data[f'{ticker2}_Pct_Change']).cumprod() - 1

    # Plot the cumulative returns
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data[f'{ticker1}_Cumulative'], mode='lines', name=f'{ticker1} Cumulative Returns'))
    fig.add_trace(go.Scatter(x=data.index, y=data[f'{ticker2}_Cumulative'], mode='lines', name=f'{ticker2} Cumulative Returns'))

    # Update the layout of the figure
    fig.update_layout(
        title=f'Cumulative Returns: {ticker1} vs {ticker2}',
        xaxis_title='Date',
        yaxis_title='Cumulative Return',
        template='plotly_dark',
        height=600
    )

    return fig