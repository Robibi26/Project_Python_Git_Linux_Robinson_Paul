
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
    "Choisissez la période des données :",
    ["1mo", "3mo", "6mo", "1y","3y"] 
    )

    ticker = "EURUSD=X"  #  EUR/USD ticker
    data = get_data(ticker,period)

    
    st.write(data) # Display data 

    # Display of price chart of EUR/USD
    fig, ax = plt.subplots()
    ax.plot(data.index, data['Close'], label="EUR/USD - Prix de clôture")
    ax.set_title(f"Graphique des prix de la paire EUR/USD ({period})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Prix de Clôture")
    ax.legend()
    st.pyplot(fig)

    #Strategy selection
    strategy = st.selectbox(
    "Choisissez une stratégie d'investissement :",
    ["Buy and Hold", "Momentum"]
)

    # Performance metrics 
    def calculate_metrics(data):
        daily_returns = data['Close'].pct_change() # Compute of daily returns 

        # Sharpe ratio
        sharpe_ratio = daily_returns.mean() / daily_returns.std()

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
    st.write(f"Rendement Moyen : {average_return:.2f}")
    st.write(f"Volatilité : {volatility:.2f}")

    # Buy and Hold strategy
    if strategy == "Buy and Hold":
        data['Buy_and_Hold'] = data['Close'] / data['Close'].iloc[0]
        st.write("Stratégie Buy and Hold")
        st.line_chart(data[['Close', 'Buy_and_Hold']])
    
    # Momentum strategy
    elif strategy == "Momentum":
        window = st.slider("Momentum window (days)", 2, 30, 5)
        data['Momentum'] = data['Close'].pct_change(periods=window)
        st.write("Stratégie Momentum")
        st.line_chart(data[['Close', 'Momentum']])

else:
    st.subheader("Module Portfolio Multi-Assets")
    st.write("Ici on affichera le portefeuille (ex : LVMH + TotalEnergies + Airbus).")
