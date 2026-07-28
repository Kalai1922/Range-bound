import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide", page_title="Strategy 1 Scanner")

st.title("📈 Strategy 1: Range-Bound Swing Scanner")
st.write("Finds stocks in a consolidated range with 20%+ width near support with YoY financial growth.")

# Watchlist input
symbols_input = st.text_input(
    "Enter Stock Symbols (separated by commas)", 
    "RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, TATAMOTORS.NS, AAPL, MSFT"
)

tickers = [s.strip() for s in symbols_input.split(",") if s.strip()]

if st.button("Run Strategy 1 Scan"):
    results = []
    
    with st.spinner("Scanning market data..."):
        for symbol in tickers:
            try:
                stock = yf.Ticker(symbol)
                df = stock.history(period="1y")
                
                if df.empty or len(df) < 100:
                    continue

                recent_high = df['High'].max()
                recent_low = df['Low'].min()
                current_price = df['Close'].iloc[-1]

                # Check 20% minimum range width
                range_width = ((recent_high - recent_low) / recent_low) * 100
                if range_width < 20.0:
                    continue

                # Check if price is near support (within 4.5% of bottom)
                if current_price <= (recent_low * 1.045):
                    
                    # Fundamental check
                    financials = stock.quarterly_financials
                    sales_growth = "N/A"
                    
                    if not financials.empty and financials.shape[1] >= 4:
                        rev_row = [i for i in financials.index if 'Revenue' in i or 'Total Revenue' in i]
                        if rev_row:
                            r_now = financials.loc[rev_row[0]].iloc[0]
                            r_prev = financials.loc[rev_row[0]].iloc[3] if len(financials.loc[rev_row[0]]) > 3 else None
                            if r_now and r_prev and r_prev > 0:
                                g = ((r_now - r_prev) / r_prev) * 100
                                sales_growth = f"{g:.1f}%"

                    results.append({
                        "Symbol": symbol,
                        "Current Price": f"₹{current_price:.2f}" if ".NS" in symbol else f"${current_price:.2f}",
                        "Support": round(recent_low, 2),
                        "Resistance": round(recent_high, 2),
                        "Range Width": f"{range_width:.1f}%",
                        "YoY Revenue Growth": sales_growth,
                        "Upside Target": f"{((recent_high - current_price) / current_price) * 100:.1f}%"
                    })
            except Exception:
                continue

    if results:
        res_df = pd.DataFrame(results)
        st.success(f"Found {len(res_df)} stock(s) matching Strategy 1!")
        st.dataframe(res_df, use_container_width=True)
    else:
        st.info("No stocks currently match all criteria. Try adding more tickers.")

