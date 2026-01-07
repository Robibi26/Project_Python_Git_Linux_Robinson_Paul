
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title="Quant Dashboard CAC 40", layout="wide")

st.title("Quant Dashboard – CAC 40")
st.write("Welcome to our project : single asset + portfolio (LVMH, TotalEnergies, Airbus).")

st.header("Choose your module")
module = st.radio(
    "Module",
    ["Single Asset (Quant A)", "Portfolio Multi-Assets (Quant B)"]
)



if module == "Single Asset (Quant A)":
    st.subheader("Single Asset Module")
    st.write("Here we display strategies on the EUR/USD currency pair.")

    def get_data(ticker,period):
        asset = yf.Ticker(ticker)
        data = asset.history(period=period, interval="1d") 
        return data
    
    # Period selection 
    period = st.selectbox(
    "Select the data period :",
    ["1mo", "3mo", "6mo", "1y","3y"] 
    )

    ticker = "EURUSD=X"  #  EUR/USD ticker
    data = get_data(ticker,period)

    
    st.write(data) # Display data 

    #Strategy selection
    strategy = st.selectbox(
    "Choose an investment strategy :",
    ["Buy and Hold", "Momentum"])

    close = data["Close"]#Closing prices

    data["Price_norm"] = close / close.iloc[0] # Normalized prices
    
    # Buy and Hold strategy
    if strategy == "Buy and Hold":        
        data["Strategy_value"] = data["Price_norm"]
    
    # Momentum strategy
    elif strategy == "Momentum":
        window = st.slider("Momentum window (days)", 2, 30, 5)

        # Trading signal:
        # 1 = we invest if the price increased over the last 'window' days
        # 0 = we do not invest 
        signal = (close.pct_change(window) > 0).astype(int)

       
        daily_returns = close.pct_change()

        # Strategy returns (with one day delay):
        # if signal = 1 : we take the daily return
        # if signal = 0 : return is 0 (we stay out of the marke
        strategy_returns = signal.shift(1) * daily_returns

        # Cumulative strategy value 
        data["Strategy_value"] = (1 + strategy_returns.fillna(0)).cumprod()
        
    fig, ax = plt.subplots()
    ax.plot(data.index, data["Price_norm"], label="EUR/USD (normalized price)")
    ax.plot(data.index, data["Strategy_value"], label=f"Strategy value ({strategy})")
    ax.set_title(f"Price vs strategy ({period})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized value")
    ax.legend()
    st.pyplot(fig)

    # Performance metrics 
    def calculate_metrics(data):
        daily_returns = data['Close'].pct_change().dropna() # Compute of daily returns 

        # Sharpe ratio
        sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * (252 ** 0.5) # Annualized Sharpe ratio

        # Max Drawdown
        cumulative_returns = (1 + daily_returns).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()

        # Average return 
        average_return = daily_returns.mean()

        # Volatility
        volatility = daily_returns.std()

        return sharpe_ratio, max_drawdown, average_return, volatility

    # Compute and display metrics
    sharpe_ratio, max_drawdown, average_return,volatility = calculate_metrics(data)

    st.write(f"Sharpe Ratio : {sharpe_ratio:.2f}")
    st.write(f"Max Drawdown : {max_drawdown:.2f}")
    st.write(f"Mean return : {average_return:.6f}")
    st.write(f"Volatility : {volatility:.6f}")

else:
    st.subheader("Module Portfolio Multi-Assets")
    st.write("Ici on affichera le portefeuille (ex : LVMH + TotalEnergies + Airbus).")
