import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title('Moving Averages Trading Strategy Backtest')

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Calculate moving averages
    data['MA1'] = data['Close'].rolling(window=10).mean()
    data['MA2'] = data['Close'].rolling(window=20).mean()
    data['MA3'] = data['Close'].rolling(window=30).mean()

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

    # Plot the cumulative returns
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(data['cumulative_return'], label='Strategy Returns')
    ax.set_xlabel('Trade Number')
    ax.set_ylabel('Cumulative Returns')
    ax.legend()

    st.pyplot(fig)
