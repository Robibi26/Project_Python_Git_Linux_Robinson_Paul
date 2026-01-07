
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Quant Dashboard CAC 40", layout="wide")

st.title("Quant Dashboard – CAC 40")
st.write("Welcome to our project : 

# Parameters and data for CAC40 assets
CAC40_ASSETS = {
    "LVMH": "MC.PA",
    "TotalEnergies": "TTE.PA",
    "Airbus": "AIR.PA",
    "Sanofi": "SAN.PA",
    "L'Oréal": "OR.PA",
    "BNP Paribas": "BNP.PA"
}

@st.cache_data
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
st.header("Choisis ton module")
module = st.radio(
    "Module",
    ["Single Asset (Quant A)", "Portfolio Multi-Assets (Quant B)"]
)


# Quant A : Single asset 
if module == "Single Asset (Quant A)":
    st.subheader("Module Single Asset")
    st.write("Ici votre binôme affichera les stratégies sur une action du CAC 40 (ex : LVMH).")
    st.info("Ton binôme pourra coder ici plus tard (backtest, graph, metrics).")

# Quant B : Multi assets
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

    # 2) Wheigts choice
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

    st.subheader("Cumulate performance of the portfolio")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(cum_perf, label="Portfolio")
    ax.set_title("Cumulated performance")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulated value")
    ax.legend()
    st.pyplot(fig)

    # Correlation Matrix
    st.subheader("Correlation Matrix")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.heatmap(returns.corr(), annot=True, cmap="Blues", ax=ax2)
    st.pyplot(fig2)

    # 6) Metrics
    st.subheader("Portfolio metrics")
    sharpe = sharpe_ratio(port_returns)
    vol = port_returns.std() * np.sqrt(252)
    mdd = max_drawdown(cum_perf)

    col1, col2, col3 = st.columns(3)
    col1.metric("Sharpe Ratio", f"{sharpe:.2f}")
    col2.metric("Annualized volatikity", f"{vol:.2%}")
    col3.metric("Max Drawdown", f"{mdd:.2%}")

