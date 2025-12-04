
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title="Quant Dashboard CAC 40", layout="wide")

st.title("Quant Dashboard – CAC 40")
st.write("Bienvenue sur notre projet : single asset + portfolio (LVMH, TotalEnergies, Airbus).")

st.header("Choisis ton module")
module = st.radio(
    "Module",
    ["Single Asset (Quant A)", "Portfolio Multi-Assets (Quant B)"]
)



if module == "Single Asset (Quant A)":
    st.subheader("Module Single Asset")
    st.write("Ici on affichera les stratégies sur la paire EUR/USD.")

    def get_data(ticker,period):
        asset = yf.Ticker(ticker)  # Utilisation du ticker
        data = asset.history(period=period, interval="1d")  # Récupère un mois de données
        return data

    period = st.selectbox(
    "Choisissez la période des données :",
    ["1mo", "3mo", "6mo", "1y","3y"]  # Périodes disponibles : 1 mois, 3 mois, 6 mois, 1 an
    )

    ticker = "EURUSD=X"  # Ticker pour EUR/USD
    data = get_data(ticker,period)

    
    st.write(data) #On affiche les données 

    # Affichage du graphique des prix de l'EUR/USD
    fig, ax = plt.subplots()
    ax.plot(data.index, data['Close'], label="EUR/USD - Prix de clôture")
    ax.set_title(f"Graphique des prix de la paire EUR/USD ({period})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Prix de Clôture")
    ax.legend()
    st.pyplot(fig)

    strategy = st.selectbox(
    "Choisissez une stratégie d'investissement :",
    ["Buy and Hold", "Momentum"]
)

    # Calcul des métriques de performance
    def calculate_metrics(data):
        daily_returns = data['Close'].pct_change()  # Calcul des rendements quotidiens

        # Calcul du sharpe ratio
        sharpe_ratio = daily_returns.mean() / daily_returns.std()

        # Calcul du Max Drawdown
        cumulative_returns = (1 + daily_returns).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()

        # Calcul du Rendement moyen
        average_return = daily_returns.mean()

        # Calcul de la volatilité
        volatility = daily_returns.std()

        return sharpe_ratio, max_drawdown, average_return, volatility

    # Calcul des métriques et affichage
    sharpe_ratio, max_drawdown, average_return,volatility = calculate_metrics(data)

    st.write(f"Sharpe Ratio : {sharpe_ratio:.2f}")
    st.write(f"Max Drawdown : {max_drawdown:.2f}")
    st.write(f"Rendement Moyen : {average_return:.2f}")
    st.write(f"Volatilité : {volatility:.2f}")

    # Stratégie Buy and Hold
    if strategy == "Buy and Hold":
        # Stratégie Buy and Hold : acheter et conserver
        data['Buy_and_Hold'] = data['Close'] / data['Close'].iloc[0]
        st.write("Stratégie Buy and Hold")
        st.line_chart(data[['Close', 'Buy_and_Hold']])

    elif strategy == "Momentum":
        # Stratégie Momentum : rendement sur 5 jours
        data['Momentum'] = data['Close'].pct_change(periods=5)  # Momentum sur 5 jours
        st.write("Stratégie Momentum")
        st.line_chart(data[['Close', 'Momentum']])

else:
    st.subheader("Module Portfolio Multi-Assets")
    st.write("Ici on affichera le portefeuille (ex : LVMH + TotalEnergies + Airbus).")
