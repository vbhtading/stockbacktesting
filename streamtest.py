import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title('Moving Averages Trading Strategy Backtest')

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Inputs for the moving averages
ma1 = st.sidebar.slider('First Moving Average', 1, 100, 10)
ma2 = st.sidebar.slider('Second Moving Average', 1, 100, 20)
ma3 = st.sidebar.slider('Third Moving Average', 1, 100, 30)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Calculate moving averages
    data['MA1'] = data['Close'].rolling(window=ma1).mean()
    data['MA2'] = data['Close'].rolling(window=ma2).mean()
    data['MA3'] = data['Close'].rolling(window=ma3).mean()

    # Define a signal (buy=1 , sell=-1, do nothing=0)
    data['signal'] = 0
    data.loc[(data['MA1'] > data['MA2']) & (data['Close'] > data['MA3']), 'signal'] = 1
    data.loc[data['Close'] < data['MA3'], 'signal'] = -1

    # Calculate daily returns
    data['return'] = data['Close'].pct_change()

    # Calculate strategy returns
    data['strategy_return'] = data['return'] * data['signal']

    # Calculate cumulative returns
    data['cumulative_return'] = (1 + data['strategy_return']).cumprod() - 1

    # Calculate number of trades, profitable trades, loss trades and total cumulative profit
    trades = data['signal'].abs().sum()
    profitable_trades = data[data['strategy_return'] > 0]['strategy_return'].count()
    loss_trades = data[data['strategy_return'] < 0]['strategy_return'].count()
    total_cumulative_profit = data['strategy_return'].sum()

    # Create a DataFrame for the summary
    summary = pd.DataFrame({
        'Total Trades': [trades],
        'Profitable Trades': [profitable_trades],
        'Loss Trades': [loss_trades],
        'Total Cumulative Profit': [total_cumulative_profit]
    })

    st.subheader("Summary for Strategy 1")
    st.table(summary)

    # Second strategy
    data['MA1_2'] = data['Close'].rolling(window=ma1+5).mean()
    data['MA2_2'] = data['Close'].rolling(window=ma2+5).mean()
    data['MA3_2'] = data['Close'].rolling(window=ma3+5).mean()

    data['signal_2'] = 0
    data.loc[(data['MA1_2'] > data['MA2_2']) & (data['Close'] > data['MA3_2']), 'signal_2'] = 1
    data.loc[data['Close'] < data['MA3_2'], 'signal_2'] = -1

    data['strategy_return_2'] = data['return'] * data['signal_2']
    data['cumulative_return_2'] = (1 + data['strategy_return_2']).cumprod() - 1

    trades_2 = data['signal_2'].abs().sum()
    profitable_trades_2 = data[data['strategy_return_2'] > 0]['strategy_return_2'].count()
    loss_trades_2 = data[data['strategy_return_2'] < 0]['strategy_return_2'].count()
    total_cumulative_profit_2 = data['strategy_return_2'].sum()

    summary_2 = pd.DataFrame({
        'Total Trades': [trades_2],
        'Profitable Trades': [profitable_trades_2],
        'Loss Trades': [loss_trades_2],
        'Total Cumulative Profit': [total_cumulative_profit_2]
    })

    st.subheader("Summary for Strategy 2")
    st.table(summary_2)

    # Plot the cumulative returns
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(data['cumulative_return'], label='Strategy Returns')
    ax.plot(data['cumulative_return_2'], label='Strategy Returns 2')

    ax.set_xlabel('Trade Number')
    ax.set_ylabel('Cumulative Returns')
    ax.legend()

    st.pyplot(fig)
