
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Quant Dashboard CAC 40", layout="wide")

st.title("Quant Dashboard – CAC 40")

st.write("Welcome to our project: Single Asset (EUR/USD) + CAC40 Portfolio Dashboard.")

if st.button("Refresh data"):
    st.cache_data.clear()
    
# Parameters and data for CAC40 assets
CAC40_ASSETS = {
    "LVMH": "MC.PA",
    "TotalEnergies": "TTE.PA",
    "Airbus": "AIR.PA",
    "Sanofi": "SAN.PA",
    "L'Oréal": "OR.PA",
    "BNP Paribas": "BNP.PA"
}

@st.cache_data(ttl=300)  # cache 5 minutes
def load_prices(tickers, start="2018-01-01"):
    data = yf.download(tickers, start=start)["Close"]
    return data.dropna()

def portfolio_performance(returns, weights):
    port_returns = (returns * weights).sum(axis=1)
    cum_perf = (1 + port_returns).cumprod()
    return port_returns, cum_perf

def sharpe_ratio(returns, risk_free=0.01):
    excess = returns - risk_free/252
    return np.sqrt(252) * excess.mean() / excess.std()

def max_drawdown(cum_returns):
    peak = cum_returns.cummax()
    drawdown = (cum_returns - peak) / peak
    return drawdown.min()

# Module choice
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

    st.subheader("Data loading")
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
    st.subheader("Performance metrics")
    sharpe_ratio, max_drawdown, average_return,volatility = calculate_metrics(data)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
    col2.metric("Volatility", f"{volatility:.2%}")
    col3.metric("Max Drawdown", f"{max_drawdown:.2%}")
    col4.metric("Mean return", f"{average_return:.6%}")
    




else:
    st.subheader("Quant B: Portfolio Multi-Assets")

    st.write("""
    Construction of a CAC40 assets portfolio :
    """)

    # Assets selection
    selected_assets = st.multiselect(
        "Choose the assets",
        list(CAC40_ASSETS.keys()),
        default=["LVMH", "TotalEnergies", "Airbus"]
    )

    if len(selected_assets) < 2:
        st.warning("Select at least two assets.")
        st.stop()

    tickers = [CAC40_ASSETS[a] for a in selected_assets]

    # Wheigts choice
    st.subheader(" Wheight of asset in the portfolio")
    weights = []
    total_weight = 0

    for asset in selected_assets:
        w = st.slider(f"Wheight of {asset}", 0.0, 1.0, 1.0 / len(selected_assets))
        weights.append(w)
        total_weight += w

    weights = np.array(weights)

    if not np.isclose(total_weight, 1.0):
        # We normalize in order to obtain the sum equal to 1    
        weights = weights / weights.sum()
        st.info("Wheights have been normalized to sum to 1.")

    # Prices loading
    st.subheader("Data loading")
    data = load_prices(tickers)
    returns = data.pct_change().dropna()

    st.write("Data loaded for :", ", ".join(selected_assets))
    st.dataframe(data.tail())

    # Portfolio performance
    port_returns, cum_perf = portfolio_performance(returns, weights)
    cum_perf_base100 = cum_perf * 100
    st.subheader("Cumulative performance of the portfolio (Base 100)")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(cum_perf_base100, label="Portfolio (Base 100)")
    ax.set_title("Cumulative performance")
    ax.set_xlabel("Date")
    ax.set_ylabel("Base 100")
    ax.legend()
    st.pyplot(fig)

    st.subheader("Assets and Portfolio cumulative value")

    base100_assets = (data / data.iloc[0]) * 100
    base100_port = cum_perf * 100

    fig_main, ax_main = plt.subplots(figsize=(12, 5))

    # Plot assets
    for col in base100_assets.columns:
        ax_main.plot(base100_assets.index, base100_assets[col], alpha=0.7, linewidth=1,label=col)

    # Plot portfolio
    ax_main.plot(base100_port.index, base100_port.values, linewidth=2.8, label="Portfolio (base 100)")

    ax_main.set_title("Assets and Portfolio cumulative value")
    ax_main.set_xlabel("Date")
    ax_main.set_ylabel("Base 100")
    ax_main.legend()
    st.pyplot(fig_main)

    # Correlation Matrix
    st.subheader("Correlation Matrix")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.heatmap(returns.corr(), annot=True, cmap="Blues", ax=ax2)
    st.pyplot(fig2)

    # Metrics
    st.subheader("Portfolio metrics")
    sharpe = sharpe_ratio(port_returns)
    vol = port_returns.std() * np.sqrt(252)
    mdd = max_drawdown(cum_perf)

    col1, col2, col3 = st.columns(3)
    col1.metric("Sharpe Ratio", f"{sharpe:.2f}")
    col2.metric("Annualized volatility", f"{vol:.2%}")
    col3.metric("Max Drawdown", f"{mdd:.2%}")

