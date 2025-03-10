import streamlit as st
import pandas as pd
from alice_client import initialize_alice
from stock_analysis import get_stocks_3_to_5_percent_up
from stock_lists import STOCK_LISTS

# Initialize AliceBlue API
st.write("Initializing AliceBlue API...")  # Show in UI for debugging
try:
    alice = initialize_alice()
    st.success("AliceBlue API initialized successfully! ✅")
except Exception as e:
    st.error(f"Error initializing AliceBlue API: {e}")
    st.stop()  # Stop execution if API initialization fails

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_stocks(tokens):
    """Fetch stocks that are up 3-5%."""
    try:
        st.write(f"Fetching stocks for tokens: {tokens}")
        stocks = get_stocks_3_to_5_percent_up(alice, tokens)
        return stocks if stocks else []
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return []

# Streamlit Setup
st.set_page_config(page_title="Stock Screener", layout="wide")
st.title("📈 Stock Screener - Daily Gainers")

# Stock List Selection
with st.expander("📋 Select Stock List:", expanded=True):
    selected_list = st.selectbox("Choose from the list", list(STOCK_LISTS.keys()))

# Start Screening Button
if st.button("🚀 Start Screening"):
    tokens = STOCK_LISTS[selected_list]
    
    with st.spinner("Fetching stock data... Please wait. ⏳"):
        stocks_up_3_to_5 = fetch_stocks(tokens)  # Cached API call
    
    if stocks_up_3_to_5:
        df = pd.DataFrame(stocks_up_3_to_5, columns=["Name", "Token", "Close", "Change (%)"])
        st.write(f"### Stocks 3-5% Up in **{selected_list}**:")
        st.dataframe(df.style.format({"Close": "{:.2f}", "Change (%)": "{:.2f}"}))
    else:
        st.warning(f"No stocks in **{selected_list}** met the 3-5% criteria. 🧐")
