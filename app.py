import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide", page_title="Strategy 1 Scanner")

st.title("📈 Strategy 1: Range-Bound Swing Scanner")
st.write("Scans stocks in a 20%+ consolidated range near support, strictly filtered for **improving YoY Revenue & Net Profit**.")

# Built-in Stock Lists (Crash-Proof)
NIFTY_50 = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS",
    "INFY.NS", "ITC.NS", "SBIN.NS", "LTIM.NS", "LT.NS", "HINDUNILVR.NS",
    "AXISBANK.NS", "KOTAKBANK.NS", "HCLTECH.NS", "M&M.NS", "SUNPHARMA.NS",
    "TATAMOTORS.NS", "MARUTI.NS", "NTPC.NS", "POWERGRID.NS", "TITAN.NS",
    "ULTRACEMCO.NS", "ASIANPAINT.NS", "ADANIENT.NS", "BAJFINANCE.NS",
    "BAJAJFINSV.NS", "ONGC.NS", "TATASTEEL.NS", "JSWSTEEL.NS", "ADANIPORTS.NS",
    "COALINDIA.NS", "GRASIM.NS", "TECHM.NS", "BPCL.NS", "HDFCLIFE.NS",
    "HEROMOTOCO.NS", "EICHERMOT.NS", "DRREDDY.NS", "CIPLA.NS", "APOLLOHOSP.NS",
    "WIPRO.NS", "DIVISLAB.NS", "TATACONSUM.NS", "SBILIFE.NS", "BRITANNIA.NS",
    "BEL.NS", "TRENT.NS", "NESTLEIND.NS", "BAJAJ-AUTO.NS", "SHRIRAMFIN.NS"
]

NIFTY_BANK = [
    "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS", 
    "INDUSINDBK.NS", "BANKBARODA.NS", "PNB.NS", "AUBANK.NS", "IDFCFIRSTB.NS",
    "FEDERALBNK.NS", "BANDHANBNK.NS"
]

NIFTY_IT = [
    "TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS",
    "LTIM.NS", "PERSISTENT.NS", "COFORGE.NS", "MPHASIS.NS", "LTTS.NS"
]

# Stock Selection Dropdown
option = st.selectbox(
    "Select Stock Universe to Scan:",
    ["Nifty 50", "Nifty Bank", "Nifty IT", "Custom Tickers"]
)

if option == "Nifty 50":
    tickers = NIFTY_50
elif option == "Nifty Bank":
    tickers = NIFTY_BANK
elif option == "Nifty IT":
    tickers = NIFTY_IT
else:
    symbols_input = st.text_input(
        "Enter Custom Tickers (separated by commas)", 
        "RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, TATAMOTORS.NS"
    )
    tickers = [s.strip() for s in symbols_input.split(",") if s.strip()]

st.info(f"Loaded {len(tickers)} stocks for scanning.")

if st.button("Run Strategy 1 Scan"):
    results = []
    
    with st.spinner("Scanning technical range & verifying financial growth..."):
        for symbol in tickers:
            try:
                stock = yf.Ticker(symbol)
                df = stock.history(period="1y")
                
                if df.empty or len(df) < 100:
                    continue

                recent_high = df['High'].max()
                recent_low = df['Low'].min()
                current_price = df['Close'].iloc[-1]

                # Rule 1: Minimum 20% Range Width
                range_width = ((recent_high - recent_low) / recent_low) * 100
                if range_width < 20.0:
                    continue

                # Rule 2: Near Support Check (within 4.5% margin of bottom)
                if current_price <= (recent_low * 1.045):
                    
                    # Rule 3: Fundamental Filter (Revenue & Net Profit YoY Growth)
                    financials = stock.quarterly_financials
                    
                    sales_growth = "N/A"
                    profit_growth = "N/A"
                    is_fundamentally_improving = False

                    if not financials.empty and financials.shape[1] >= 4:
                        rev_rows = [i for i in financials.index if 'Revenue' in i or 'Total Revenue' in i]
                        profit_rows = [i for i in financials.index if 'Net Income' in i or 'Net Income Common Stockholders' in i]

                        s_growth_val = None
                        p_growth_val = None

                        if rev_rows:
                            r_now = financials.loc[rev_rows[0]].iloc[0]
                            r_prev = financials.loc[rev_rows[0]].iloc[3] if len(financials.loc[rev_rows[0]]) > 3 else None
                            if pd.notna(r_now) and pd.notna(r_prev) and r_prev > 0:
                                s_growth_val = ((r_now - r_prev) / r_prev) * 100
                                sales_growth = f"{s_growth_val:.1f}%"

                        if profit_rows:
                            p_now = financials.loc[profit_rows[0]].iloc[0]
                            p_prev = financials.loc[profit_rows[0]].iloc[3] if len(financials.loc[profit_rows[0]]) > 3 else None
                            if pd.notna(p_now) and pd.notna(p_prev) and p_prev > 0:
                                p_growth_val = ((p_now - p_prev) / p_prev) * 100
                                profit_growth = f"{p_growth_val:.1f}%"

                        if (s_growth_val is not None and s_growth_val > 0) or (p_growth_val is not None and p_growth_val > 0):
                            is_fundamentally_improving = True

                    if is_fundamentally_improving:
                        results.append({
                            "Symbol": symbol,
                            "Current Price": f"₹{current_price:.2f}" if ".NS" in symbol else f"${current_price:.2f}",
                            "Support Level": round(recent_low, 2),
                            "Resistance Level": round(recent_high, 2),
                            "Range Width": f"{range_width:.1f}%",
                            "YoY Revenue Growth": sales_growth,
                            "YoY Net Profit Growth": profit_growth,
                            "Target Upside": f"{((recent_high - current_price) / current_price) * 100:.1f}%"
                        })
            except Exception:
                continue

    if results:
        res_df = pd.DataFrame(results)
        st.success(f"Found {len(res_df)} stock(s) matching Strategy 1!")
        st.dataframe(res_df, use_container_width=True)
    else:
        st.info("No stocks currently match both technical range rules AND fundamental growth criteria.")
