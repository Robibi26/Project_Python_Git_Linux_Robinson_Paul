
import streamlit as st

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
    st.write("Ici on affichera les stratégies sur une action du CAC 40 (ex : LVMH).")
else:
    st.subheader("Module Portfolio Multi-Assets")
    st.write("Ici on affichera le portefeuille (ex : LVMH + TotalEnergies + Airbus).")
