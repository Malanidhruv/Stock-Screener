import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_stock_data(alice, token):
    """Fetch historical data and check if the stock gained 3-5%."""
    try:
        instrument = alice.get_instrument_by_token('NSE', token)

        to_datetime = datetime.now()
        from_datetime = to_datetime - timedelta(days=5)
        interval = "D"

        historical_data = alice.get_historical(instrument, from_datetime, to_datetime, interval)
        df = pd.DataFrame(historical_data)

        if len(df) < 2:
            return None  # Not enough data

        yesterday_close = df['close'].iloc[-1]
        day_before_close = df['close'].iloc[-2]
        pct_change = ((yesterday_close - day_before_close) / day_before_close) * 100

        if 2 <= pct_change <= 5:
            return {
                'Name': instrument.name,
                'Token': token,
                'Close': yesterday_close,
                'Change (%)': pct_change
            }

    except Exception as e:
        print(f"Error processing token {token}: {e}")
    
    return None

def get_stocks_3_to_5_percent_up(alice, tokens):
    """Fetch stocks that gained 3-5% using multithreading."""
    stocks_up_3_to_5 = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_token = {executor.submit(fetch_stock_data, alice, token): token for token in tokens}
        
        for future in as_completed(future_to_token):
            result = future.result()
            if result:
                stocks_up_3_to_5.append(result)

    return stocks_up_3_to_5
