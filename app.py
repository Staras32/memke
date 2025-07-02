import streamlit as st
import requests

MIN_LP_SOL = 50  # Tavo minimalus likvidumas eurais ar USD (pakeisk pagal poreikį)

@st.cache_data(ttl=60)
def get_data():
    url = "https://api.dexscreener.com/latest/dex/tokens/solana"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        pairs = data.get("pairs", [])
        # Tikrinam, kad tai dict ir turi liquidityUsd
        pairs_filtered = [p for p in pairs if isinstance(p, dict) and p.get("liquidityUsd")]
        return pairs_filtered
    except Exception as e:
        st.error(f"Klaida traukiant duomenis: {e}")
        return []

st.title("Solana Memecoin Filter")

tokens = get_data()

filtered_tokens = []
for t in tokens:
    liquidity = t.get("liquidityUsd", 0)
    if liquidity / 20 >= MIN_LP_SOL:
        filtered_tokens.append(t)

st.write(f"Iš viso gauta tokenų: {len(tokens)}")
st.write(f"Filtruotų tokenų su likvidumu > {MIN_LP_SOL * 20}: {len(filtered_tokens)}")

for token in filtered_tokens:
    name = token.get("pairName", "Nežinomas")
    liquidity = token.get("liquidityUsd", 0)
    st.write(f"**{name}** — likvidumas: ${liquidity:,.2f}")

if st.button("Atnaujinti"):
    st.experimental_rerun()
