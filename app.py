import streamlit as st
import pandas as pd
from alice_client import initialize_alice
from stock_analysis import get_stocks_3_to_5_percent_up
from stock_lists import STOCK_LISTS

# Initialize AliceBlue API
alice = initialize_alice()

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_stocks(tokens):
    return get_stocks_3_to_5_percent_up(alice, tokens)

# Streamlit Setup
st.set_page_config(page_title="Stock Screener", layout="wide")
st.title("📈 Stock Screener - Daily Gainers")

# Stock List Selection (Better for Mobile)
with st.expander("📋 Select Stock List:", expanded=True):
    selected_list = st.selectbox("Choose from the list", list(STOCK_LISTS.keys()))

# Start Screening Button
if st.button("🚀 Start Screening"):
    tokens = STOCK_LISTS[selected_list]
    stocks_up_3_to_5 = fetch_stocks(tokens)  # Cached API call
    
    if stocks_up_3_to_5:
        df = pd.DataFrame(stocks_up_3_to_5, columns=["Name", "Token", "Close", "Change (%)"])
        st.write(f"### Stocks 3-5% Up in **{selected_list}**:")
        st.dataframe(df.style.format({"Close": "{:.2f}", "Change (%)": "{:.2f}"}))
    else:
        st.warning(f"No stocks in **{selected_list}** met the 3-5% criteria.")
