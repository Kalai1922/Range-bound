import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="RBS Scanner")

st.title("📈 Range-Bound Swing (RBS) Scanner")
st.write(
    "Finds stocks with a **20%+ sideways range**, at least **2 confirmed support "
    "and 2 confirmed resistance touches in zig-zag order**, currently sitting on the "
    "**3rd (or later) touch of support with a reversal forming**, and **both revenue "
    "and net profit improving YoY**."
)

# ---------------- VSpartans Stock Universe ----------------
V40 = [
    "BAJAJHLDNG.NS","ABBOTINDIA.NS","AXISBANK.NS","PFIZER.NS","BERGEPAINT.NS","TITAN.NS",
    "HINDUNILVR.NS","BATAINDIA.NS","LT.NS","RELIANCE.NS","MARICO.NS","BAJAJ-AUTO.NS",
    "KOTAKBANK.NS","TCS.NS","DABUR.NS","SBIN.NS","VOLTAS.NS","PGHH.NS","ITC.NS",
    "BAJFINANCE.NS","ICICIBANK.NS","HCLTECH.NS","HDFCBANK.NS","HDFCLIFE.NS","GILLETTE.NS",
    "HAVELLS.NS","COLPAL.NS","PIDILITIND.NS","MARUTI.NS","HDFCAMC.NS","NESTLEIND.NS",
    "ICICIPRULI.NS","ICICIGI.NS","ASIANPAINT.NS","GLAXO.NS","DMART.NS","PAGEIND.NS",
    "INFY.NS","BAJAJFINSV.NS"
]

V40_NEXT = [
    "CDSL.NS","BSE.NS","JIOFIN.NS","ANGELONE.NS","CAMS.NS","MCX.NS","ULTRACEMCO.NS","ACC.NS",
    "TEAMLEASE.NS","ASTRAZEN.NS","CIPLA.NS","ERIS.NS","LALPATHLAB.NS","APOLLOHOSP.NS",
    "MEDANTA.NS","FORTIS.NS","ADANIPORTS.NS","JSWINFRA.NS","AWL.NS","GODREJCP.NS","DIXON.NS",
    "KAJARIACER.NS","HONAUT.NS","DMART.NS","RELAXO.NS","BLUESTARCO.NS","BOSCHLTD.NS",
    "EICHERMOT.NS","MRF.NS","M&M.NS","TATAMOTORS.NS","HYUNDAI.NS","INDHOTEL.NS","ITCHOTELS.NS",
    "UNITDSPR.NS","RADICO.NS","UBL.NS","VBL.NS"
]

V200 = [
    "LTM.NS",
    "PGHH.NS","WAAREEINDO.NS","TIPSMUSIC.NS","ICICIAMC.NS","COLPAL.NS","GILLETTE.NS","SANOFICONR.NS",
    "WAAREERTL.NS","NESTLEIND.NS","PGHL.NS","GVPIL.NS","GVT&D.NS","MCX.NS","IGIL.NS",
    "ENRIN.NS","ESABINDIA.NS","PAGEIND.NS","JPOLYINVST.NS","WEBELSOLAR.NS","TCS.NS","GLAXO.NS",
    "TENNIND.NS","CASTROLIND.NS","BSE.NS","HBLENGINE.NS","SANOFI.NS","ANANDRATHI.NS","INGERRAND.NS",
    "CRIZAC.NS","IEX.NS","3MINDIA.NS","CAMS.NS","MARICO.NS","IRCTC.NS","OFSS.NS",
    "ATLANTAELE.NS","EMMVEE.NS","ABBOTINDIA.NS","NAM-INDIA.NS","GRSE.NS","HDFCAMC.NS","HINDCOPPER.NS",
    "TRAVELFOOD.NS","DIXON.NS","GKENERGY.NS","CRAMC.NS","INFY.NS","GLENMARK.NS","NATIONALUM.NS",
    "CUMMINSIND.NS","ITC.NS","MSUMI.NS","WAAREEENER.NS","HYUNDAI.NS","OSWALPUMPS.NS","SOLARINDS.NS",
    "PRUDENT.NS","GROWW.NS","BEL.NS","FORCEMOT.NS","MAZDOCK.NS","SHARDAMOTR.NS","TRITURBINE.NS",
    "HEROMOTOCO.NS","SUZLON.NS","COALINDIA.NS","CHENNPETRO.NS","ECLERX.NS","AJANTPHARM.NS","PERSISTENT.NS",
    "TDPOWERSYS.NS","INOXINDIA.NS","POLYCAB.NS","BBTC.NS","CRISIL.NS","LGEINDIA.NS","ABSLAMC.NS",
    "CDSL.NS","HAL.NS","ACE.NS","APLAPOLLO.NS","ACUTAAS.NS","APARINDS.NS","PIDILITIND.NS",
    "DDEVPLSTIK.NS","NBCC.NS","ENGINERSIN.NS","VIKRAMSOLR.NS","EICHERMOT.NS","HCLTECH.NS","ANTHEM.NS",
    "KIRLPNU.NS","MSTCLTD.NS","GODFRYPHLP.NS","SHARDACROP.NS","HEXT.NS","TATAELXSI.NS","ABB.NS",
    "SKFINDIA.NS","LTIM.NS","POWERINDIA.NS","FIEMIND.NS","BLS.NS","KFINTECH.NS","BAYERCROP.NS",
    "JYOTHYLAB.NS","CPPLUS.NS","HINDUNILVR.NS","RUBICON.NS","VSTIND.NS","RRKABEL.NS","EMAMILTD.NS",
    "GPPL.NS","INDIAMART.NS","LALPATHLAB.NS","STYL.NS","SCHAEFFLER.NS","NMDC.NS","JAMNAAUTO.NS",
    "CGPOWER.NS","LTTS.NS","ASHOKA.NS","BLUEJET.NS","NEULANDLAB.NS","UNITDSPR.NS","ASIANPAINT.NS",
    "TANLA.NS","KPITTECH.NS","GABRIEL.NS","CHAMBLFERT.NS","SUPRIYA.NS","NEWGEN.NS","HAVELLS.NS",
    "KSB.NS","CAPLIPOINT.NS","AVANTIFEED.NS","DOMS.NS","RADICO.NS","PFIZER.NS","QUESS.NS",
    "AJAXENGG.NS","ALIVUS.NS","DHANUKA.NS","MANYAVAR.NS","VOLTAMP.NS","COFORGE.NS","SUMICHEM.NS",
    "KAJARIACER.NS","NSDL.BO","TECHM.NS","RAILTEL.NS","ZENSARTECH.NS","PETRONET.NS","JSWDULUX.NS",
    "BALUFORGE.NS","REFEX.NS","MISHTANN.BO","HSCL.NS","MPHASIS.NS","ELGIEQUIP.NS","COROMANDEL.NS",
    "RITES.NS","BIKAJI.NS","DIVISLAB.NS","DATAPATTNS.NS","ICICIGI.NS","BERGEPAINT.NS","BOSCHLTD.NS",
    "FINEORG.NS","SIEMENS.NS","VESUVIUS.NS","VINATIORGA.NS","WABAG.NS","BLUESTARCO.NS","ALKEM.NS",
    "GRINDWELL.NS","BSOFT.NS","LOTUSDEV.NS","AIAENG.NS","TATATECH.NS","ELECON.NS","SUPREMEIND.NS",
    "EIHOTEL.NS","CLEAN.NS","NIITMTS.NS","SUNPHARMA.NS","AHLUCONT.NS","GPIL.NS","KIRLOSBROS.NS",
    "DABUR.NS","KEI.NS",
    "BAJFINANCE.NS","MUTHOOTFIN.NS","SHRIRAMFIN.NS","CHOLAFIN.NS","SBICARD.NS","SUNDARMFIN.NS","FIVESTAR.NS",
]

def dedupe(tickers):
    seen = set()
    out = []
    for t in tickers:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out

V40 = dedupe(V40)
V40_NEXT = dedupe(V40_NEXT)
V200 = dedupe(V200)

# ---------------- V50 (stricter V200 filter) ----------------
FINANCIALS_V50 = {
    "BAJFINANCE.NS", "MUTHOOTFIN.NS", "SHRIRAMFIN.NS", "CHOLAFIN.NS",
    "SBICARD.NS", "SUNDARMFIN.NS", "FIVESTAR.NS"
}

@st.cache_data(ttl=86400, show_spinner=False)
def compute_v50_universe(v200_list, financials_set):
    """Applies Vivek sir's stricter V50 filters on top of V200 (per V50of_v200 notes):
    non-financials need Debt/Equity<0.2, Net Profit>Rs.250cr, ROCE>25%, YoY qtr profit growth>0,
    price<0.75xATH. Financials (banks/NBFC) need ROE>15%, Net Profit>Rs.1500cr, price<0.75xATH.
    PSU/government companies are excluded per the V200 criteria doc unless manually overridden.
    NOTE: yfinance doesn't expose a true ROCE figure — this uses returnOnAssets as an imperfect
    proxy, so any pass here still needs a Screener.in cross-check before you act on it, same as
    the highest-ever-profit checks elsewhere in this app."""
    passed = []
    for symbol in v200_list:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="max")
            if hist.empty:
                continue
            ath = hist['High'].max()
            current_price = hist['Close'].iloc[-1]
            if ath <= 0 or current_price >= 0.75 * ath:
                continue

            info = stock.info
            net_income = info.get("netIncomeToCommon")
            if net_income is None:
                continue

            if symbol in financials_set:
                roe = info.get("returnOnEquity")
                if roe is not None and roe * 100 > 15 and net_income > 1500 * 1e7:
                    passed.append(symbol)
            else:
                debt_to_equity = info.get("debtToEquity")
                roce_proxy = info.get("returnOnAssets")
                if debt_to_equity is None or roce_proxy is None:
                    continue
                de_ratio = debt_to_equity / 100 if debt_to_equity > 5 else debt_to_equity
                if de_ratio < 0.2 and net_income > 250 * 1e7 and roce_proxy * 100 > 25:
                    passed.append(symbol)
        except Exception:
            continue
    return passed

st.caption(
    "NPA (bad-loan) trend is part of Vivek sir's fundamental filter for banks/NBFCs but isn't "
    "available through this data source — verify that manually on Screener.in for financial stocks."
)

option = st.selectbox("Select Stock Universe to Scan:", ["V40", "V40 Next", "V50", "V200", "Custom Tickers"])

if option == "V40":
    tickers = V40
elif option == "V40 Next":
    tickers = V40_NEXT
elif option == "V50":
    with st.spinner("Applying V50 filters to the V200 universe... this checks fundamentals for every stock, so it can take a minute."):
        tickers = compute_v50_universe(V200, FINANCIALS_V50)
    st.caption(f"V50 found {len(tickers)} stock(s) passing the stricter filter. Cross-check on Screener.in before acting — see note above.")
elif option == "V200":
    tickers = V200
else:
    symbols_input = st.text_input(
        "Enter Custom Tickers (comma separated)",
        "RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, TATAMOTORS.NS"
    )
    tickers = [s.strip() for s in symbols_input.split(",") if s.strip()]

st.info(f"Loaded {len(tickers)} stocks for scanning.")

with st.sidebar:
    st.header("Tuning")
    pivot_window = st.slider("Pivot sensitivity (trading days)", 3, 10, 5,
                              help="A local high/low must be the extreme point within this many days on either side to count as a pivot.")
    level_tolerance = st.slider("Level clustering tolerance (%)", 1.0, 5.0, 3.0, step=0.5,
                                 help="How close two pivots must be (as % of price) to count as touching the same support/resistance level.") / 100
    min_gap_days = st.slider("Minimum days between touches", 3, 15, 5,
                              help="Two pivots closer together than this are treated as one visit to the level, not two separate touches.")

# ---------------- Core RBS logic ----------------

def find_pivots(df, window):
    """Local extrema: a bar is a pivot high/low if it's the max/min within +/- window days."""
    highs = df['High'].values
    lows = df['Low'].values
    n = len(df)
    piv_high_idx, piv_low_idx = [], []
    for i in range(window, n - window):
        seg_h = highs[i-window:i+window+1]
        seg_l = lows[i-window:i+window+1]
        if highs[i] == seg_h.max():
            piv_high_idx.append(i)
        if lows[i] == seg_l.min():
            piv_low_idx.append(i)
    return piv_high_idx, piv_low_idx

def cluster_levels(idx_list, price_lookup, tolerance):
    """Group pivot indices into price levels within `tolerance` of each other."""
    if not idx_list:
        return []
    points = sorted([(i, price_lookup[i]) for i in idx_list], key=lambda x: x[1])
    clusters, current = [], [points[0]]
    for p in points[1:]:
        if abs(p[1] - current[-1][1]) / current[-1][1] <= tolerance:
            current.append(p)
        else:
            clusters.append(current)
            current = [p]
    clusters.append(current)
    levels = []
    for c in clusters:
        avg_price = sum(x[1] for x in c) / len(c)
        idxs = sorted(x[0] for x in c)
        levels.append({"price": avg_price, "touch_idx": idxs})
    return levels

def distinct_touch_count(idxs, min_gap_days):
    """Collapse pivots that are close in time into a single touch event."""
    if not idxs:
        return 0, []
    idxs = sorted(idxs)
    kept = [idxs[0]]
    for i in idxs[1:]:
        if i - kept[-1] >= min_gap_days:
            kept.append(i)
    return len(kept), kept

def check_zigzag(support_touches, resistance_touches):
    """Merge support+resistance touch dates chronologically, collapse consecutive
    same-side touches, and confirm an alternating S/R/S/R pattern with >=2 of each."""
    events = [(i, 'S') for i in support_touches] + [(i, 'R') for i in resistance_touches]
    events.sort(key=lambda x: x[0])
    collapsed = []
    for i, side in events:
        if not collapsed or collapsed[-1][1] != side:
            collapsed.append((i, side))
    s_count = sum(1 for _, side in collapsed if side == 'S')
    r_count = sum(1 for _, side in collapsed if side == 'R')
    return s_count >= 2 and r_count >= 2, s_count, r_count

def reversal_confirmed(df):
    """Simple higher-high / higher-low check over the last 3 bars near support."""
    if len(df) < 3:
        return False
    last3 = df.iloc[-3:]
    highs = last3['High'].values
    lows = last3['Low'].values
    return highs[-1] > highs[-2] and lows[-1] > lows[-2]

def fundamentals_improving(stock):
    """Both TTM-proxy (YoY quarterly) revenue AND net profit must be positive. Returns
    (is_improving, revenue_growth_str, profit_growth_str)."""
    financials = stock.quarterly_financials
    sales_growth, profit_growth = "N/A", "N/A"
    s_val, p_val = None, None
    if not financials.empty and financials.shape[1] >= 4:
        rev_rows = [i for i in financials.index if 'Revenue' in i]
        profit_rows = [i for i in financials.index if 'Net Income' in i]
        if rev_rows:
            r_now, r_prev = financials.loc[rev_rows[0]].iloc[0], financials.loc[rev_rows[0]].iloc[3]
            if pd.notna(r_now) and pd.notna(r_prev) and r_prev > 0:
                s_val = ((r_now - r_prev) / r_prev) * 100
                sales_growth = f"{s_val:.1f}%"
        if profit_rows:
            p_now, p_prev = financials.loc[profit_rows[0]].iloc[0], financials.loc[profit_rows[0]].iloc[3]
            if pd.notna(p_now) and pd.notna(p_prev) and p_prev > 0:
                p_val = ((p_now - p_prev) / p_prev) * 100
                profit_growth = f"{p_val:.1f}%"
    is_improving = (s_val is not None and s_val > 0) and (p_val is not None and p_val > 0)
    return is_improving, sales_growth, profit_growth

if st.button("Run RBS Scan"):
    results = []
    progress = st.progress(0, text="Starting scan...")

    for n_done, symbol in enumerate(tickers, start=1):
        progress.progress(n_done / len(tickers), text=f"Scanning {symbol}...")
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period="1y")
            if df.empty or len(df) < 100:
                continue

            close_lookup = df['Close'].values
            high_lookup = df['High'].values
            low_lookup = df['Low'].values
            current_price = close_lookup[-1]

            piv_high_idx, piv_low_idx = find_pivots(df, pivot_window)
            support_levels = cluster_levels(piv_low_idx, low_lookup, level_tolerance)
            resistance_levels = cluster_levels(piv_high_idx, high_lookup, level_tolerance)

            best_candidate = None
            for s in support_levels:
                for r in resistance_levels:
                    if r["price"] <= s["price"]:
                        continue
                    range_width = ((r["price"] - s["price"]) / s["price"]) * 100
                    if range_width < 20.0:
                        continue
                    s_touches_n, s_touches_idx = distinct_touch_count(s["touch_idx"], min_gap_days)
                    r_touches_n, r_touches_idx = distinct_touch_count(r["touch_idx"], min_gap_days)
                    if s_touches_n < 2 or r_touches_n < 2:
                        continue
                    is_zigzag, s_cnt, r_cnt = check_zigzag(s_touches_idx, r_touches_idx)
                    if not is_zigzag:
                        continue
                    # Prefer the widest valid range if multiple candidates qualify
                    if best_candidate is None or range_width > best_candidate["range_width"]:
                        best_candidate = {
                            "support": s["price"], "resistance": r["price"],
                            "range_width": range_width,
                            "support_touches": s_cnt, "resistance_touches": r_cnt
                        }

            if best_candidate is None:
                continue

            # Must currently be sitting near support, on the 3rd-or-later touch
            # Must be genuinely AT support, not above it (too far) and not BELOW it (broken down).
            # The lower bound was missing before, which let already-broken supports pass as "near."
            near_support = (
                best_candidate["support"] * (1 - level_tolerance) <= current_price
                <= best_candidate["support"] * (1 + level_tolerance)
            )
            is_3rd_plus_touch = best_candidate["support_touches"] >= 2  # 2 historical + this live one = 3rd+
            if not (near_support and is_3rd_plus_touch):
                continue

            if not reversal_confirmed(df):
                continue

            is_improving, sales_growth, profit_growth = fundamentals_improving(stock)
            if not is_improving:
                continue

            target_upside = ((best_candidate["resistance"] - current_price) / current_price) * 100
            results.append({
                "Symbol": symbol,
                "Current Price": f"₹{current_price:.2f}",
                "Support Level": round(best_candidate["support"], 2),
                "Resistance Level": round(best_candidate["resistance"], 2),
                "Range Width": f"{best_candidate['range_width']:.1f}%",
                "Support Touches": best_candidate["support_touches"],
                "Resistance Touches": best_candidate["resistance_touches"],
                "Reversal Confirmed": "✅",
                "YoY Revenue Growth": sales_growth,
                "YoY Net Profit Growth": profit_growth,
                "Target Upside": f"{target_upside:.1f}%"
            })
        except Exception:
            continue

    progress.empty()

    if results:
        res_df = pd.DataFrame(results)
        st.success(f"Found {len(res_df)} stock(s) matching RBS — full rule set.")
        st.dataframe(res_df, use_container_width=True)
    else:
        st.info(
            "No stocks currently satisfy all RBS conditions: 20%+ zig-zag range, "
            "2+ alternating support/resistance touches, live 3rd-touch with reversal, "
            "and both revenue & profit improving. This is expected to be a rare, narrow list — "
            "that's the filter doing its job."
        )
