import streamlit as st
import requests

st.title("Solana Memecoin Filter")

@st.cache_data(ttl=60)
def get_data():
    url = "https://api.dexscreener.com/latest/dex/tokens/solana"
    try:
        res = requests.get(url)
        data = res.json()
        return data.get("pairs", [])
    except:
        return []

tokens = get_data()

MIN_LP_SOL = 1  # filtras: minimalus LP SOL

filtered = [t for t in tokens if (t.get("liquidityUsd", 0) / 20) >= MIN_LP_SOL]
top = sorted(filtered, key=lambda x: x.get("volumeUsd", 0), reverse=True)[:10]

st.write(f"Rasta {len(top)} memecoinų su LP ≥ {MIN_LP_SOL} SOL:")

for t in top:
    name = t["baseToken"]["name"]
    symbol = t["baseToken"]["symbol"]
    lp = round(t.get("liquidityUsd", 0) / 20, 2)
    vol = round(t.get("volumeUsd", 0), 2)
    price = round(t.get("priceUsd", 0), 6)
    st.write(f"**{name}** ({symbol}): LP {lp} SOL | Volume 24h: ${vol} | Price: ${price}")
