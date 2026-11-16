
import streamlit as st
import pandas as pd
import yfinance as yf
from pathlib import Path
from io import BytesIO


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Investment Portfolio Tracker",
    page_icon="📈",
    layout="wide"
)


# ==========================================================
# 2. CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background-color: #F5F7FB;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

.hero {
    background: linear-gradient(120deg, #E8F0FF, #F4EEFF);
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 25px;
    border: 1px solid #E0E7F5;
}

.hero h1 {
    color: #172554;
    font-size: 34px;
    margin-bottom: 8px;
}

.hero p {
    color: #64748B;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #E8ECF3;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}

.stButton > button {
    background: #315EFB;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 22px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #2449CC;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. LOAD VALID S&P 500 TICKERS
# ==========================================================

@st.cache_data
def load_valid_tickers():

    file_path = Path(__file__).parent / "constituents.csv"

    if not file_path.exists():
        return None

    df = pd.read_csv(file_path)

    if "Symbol" not in df.columns:
        return None

    return set(
        df["Symbol"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
    )


# ==========================================================
# 4. FETCH LATEST STOCK PRICE
# ==========================================================

def fetch_current_price(ticker):

    try:
        yahoo_ticker = ticker.replace(".", "-")
        stock = yf.Ticker(yahoo_ticker)

        # First attempt: fast_info
        try:
            price = stock.fast_info["last_price"]

            if price is not None and pd.notna(price) and price > 0:
                return float(price), "Yahoo Finance"

        except Exception:
            pass

        # Second attempt: historical closing price
        try:
            history = stock.history(period="5d")

            if not history.empty:
                closing_prices = history["Close"].dropna()

                if not closing_prices.empty:
                    price = float(closing_prices.iloc[-1])

                    if price > 0:
                        return price, "Historical Close"

        except Exception:
            pass

    except Exception:
        pass

    return None, "Unavailable"


# ==========================================================
# 5. PORTFOLIO CALCULATIONS
# ==========================================================

def calculate_portfolio(data):

    results = []

    for stock in data:

        investment = stock["Buy Price"] * stock["Quantity"]

        current_value = (
            stock["Current Price"] * stock["Quantity"]
        )

        profit_loss = current_value - investment

        profit_loss_percentage = (
            (profit_loss / investment) * 100
            if investment != 0 else 0
        )

        results.append({
            "Ticker": stock["Ticker"],
            "Buy Price": stock["Buy Price"],
            "Quantity": stock["Quantity"],
            "Current Price": stock["Current Price"],
            "Price Source": stock["Price Source"],
            "Investment": investment,
            "Current Value": current_value,
            "Profit/Loss": profit_loss,
            "Profit/Loss Percentage": profit_loss_percentage
        })

    return pd.DataFrame(results)


# ==========================================================
# 6. CSV EXPORT
# ==========================================================

def create_csv(dataframe):

    export_df = dataframe.copy()

    total_row = {
        "Ticker": "TOTAL",
        "Buy Price": "",
        "Quantity": "",
        "Current Price": "",
        "Price Source": "",
        "Investment": export_df["Investment"].sum(),
        "Current Value": export_df["Current Value"].sum(),
        "Profit/Loss": export_df["Profit/Loss"].sum(),
        "Profit/Loss Percentage": (
            export_df["Profit/Loss"].sum()
            / export_df["Investment"].sum() * 100
            if export_df["Investment"].sum() != 0 else 0
        )
    }

    export_df = pd.concat(
        [export_df, pd.DataFrame([total_row])],
        ignore_index=True
    )

    return export_df.to_csv(index=False).encode("utf-8")


# ==========================================================
# 7. HERO SECTION
# ==========================================================

st.markdown("""
<div class="hero">
    <h1>📈 Investment Portfolio Tracker</h1>
    <p>
        Track your stock investments, monitor market value,
        and analyze your portfolio performance.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# 8. LOAD TICKER DATA
# ==========================================================

valid_tickers = load_valid_tickers()

if valid_tickers is None:

    st.error(
        "constituents.csv not found or missing the Symbol column. "
        "Please check your project folder."
    )

    st.stop()


st.caption(
    f"📊 Supporting {len(valid_tickers)} S&P 500 listed companies"
)


# ==========================================================
# 9. PORTFOLIO INPUT SECTION
# ==========================================================

st.subheader("💼 Add Your Investments")

st.write(
    "Enter the stocks you own along with their purchase price "
    "and quantity."
)

number_of_stocks = st.number_input(
    "Number of stocks in your portfolio",
    min_value=1,
    max_value=50,
    value=1,
    step=1
)


with st.form("portfolio_form"):

    stock_inputs = []

    for i in range(int(number_of_stocks)):

        st.markdown(f"**Stock {i + 1}**")

        col1, col2, col3 = st.columns(3)

        with col1:
            ticker = st.text_input(
                "Stock Ticker",
                placeholder="e.g. AAPL",
                key=f"ticker_{i}"
            )

        with col2:
            buy_price = st.number_input(
                "Buy Price ($)",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key=f"buy_{i}"
            )

        with col3:
            quantity = st.number_input(
                "Quantity",
                min_value=0,
                value=0,
                step=1,
                key=f"quantity_{i}"
            )

        stock_inputs.append({
            "Ticker": ticker.strip().upper(),
            "Buy Price": buy_price,
            "Quantity": quantity
        })

        st.divider()

    submitted = st.form_submit_button(
        "Analyze My Portfolio",
        use_container_width=True
    )


# ==========================================================
# 10. VALIDATION AND PRICE FETCHING
# ==========================================================

if submitted:

    errors = []
    seen_tickers = set()
    valid_stocks = []

    for stock in stock_inputs:

        ticker = stock["Ticker"]

        if not ticker:
            errors.append("Please enter a ticker for every stock.")
            continue

        if ticker not in valid_tickers:
            errors.append(
                f"{ticker} is not a valid S&P 500 ticker."
            )
            continue

        if ticker in seen_tickers:
            errors.append(
                f"Duplicate ticker found: {ticker}"
            )
            continue

        seen_tickers.add(ticker)

        if stock["Buy Price"] <= 0:
            errors.append(
                f"Buy price for {ticker} must be greater than zero."
            )
            continue

        if stock["Quantity"] <= 0:
            errors.append(
                f"Quantity for {ticker} must be greater than zero."
            )
            continue

        valid_stocks.append(stock)

    if errors:

        for error in errors:
            st.error(error)

    elif not valid_stocks:

        st.warning("Please enter at least one valid stock.")

    else:

        resolved_stocks = []
        unresolved_stocks = []

        progress = st.progress(0)
        status = st.empty()

        for index, stock in enumerate(valid_stocks):

            ticker = stock["Ticker"]

            status.write(
                f"Fetching current price for {ticker}..."
            )

            current_price, source = fetch_current_price(ticker)

            if current_price is not None:

                stock["Current Price"] = current_price
                stock["Price Source"] = source

                resolved_stocks.append(stock)

            else:

                unresolved_stocks.append(stock)

            progress.progress(
                (index + 1) / len(valid_stocks)
            )

        status.empty()
        progress.empty()

        st.session_state["resolved_stocks"] = resolved_stocks
        st.session_state["unresolved_stocks"] = unresolved_stocks
        st.session_state["portfolio_submitted"] = True


# ==========================================================
# 11. MANUAL PRICE FALLBACK
# ==========================================================

if st.session_state.get("portfolio_submitted", False):

    resolved_stocks = st.session_state.get(
        "resolved_stocks", []
    )

    unresolved_stocks = st.session_state.get(
        "unresolved_stocks", []
    )

    if unresolved_stocks:

        st.warning(
            "Live price could not be fetched for some stocks. "
            "Please enter their current prices manually."
        )

        with st.form("manual_price_form"):

            manual_prices = {}

            for stock in unresolved_stocks:

                manual_prices[stock["Ticker"]] = st.number_input(
                    f"Current Price for {stock['Ticker']} ($)",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                    key=f"manual_{stock['Ticker']}"
                )

            manual_submitted = st.form_submit_button(
                "Complete Portfolio Analysis"
            )

        if manual_submitted:

            missing_prices = [
                ticker
                for ticker, price in manual_prices.items()
                if price <= 0
            ]

            if missing_prices:

                st.error(
                    "Please enter a valid current price for: "
                    + ", ".join(missing_prices)
                )

            else:

                for stock in unresolved_stocks:

                    stock["Current Price"] = manual_prices[
                        stock["Ticker"]
                    ]

                    stock["Price Source"] = "Manual Entry"

                    resolved_stocks.append(stock)

                st.session_state["resolved_stocks"] = resolved_stocks
                st.session_state["unresolved_stocks"] = []
                st.session_state["analysis_complete"] = True

                st.rerun()

    else:

        st.session_state["analysis_complete"] = True


# ==========================================================
# 12. DISPLAY PORTFOLIO RESULTS
# ==========================================================

if st.session_state.get("analysis_complete", False):

    portfolio_df = calculate_portfolio(
        st.session_state["resolved_stocks"]
    )

    total_investment = portfolio_df["Investment"].sum()
    total_current_value = portfolio_df["Current Value"].sum()
    total_profit_loss = portfolio_df["Profit/Loss"].sum()

    total_percentage = (
        (total_profit_loss / total_investment) * 100
        if total_investment != 0 else 0
    )

    st.divider()

    st.subheader("📊 Portfolio Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Investment",
        f"${total_investment:,.2f}"
    )

    col2.metric(
        "Current Value",
        f"${total_current_value:,.2f}"
    )

    col3.metric(
        "Total Profit / Loss",
        f"${total_profit_loss:,.2f}",
        delta=f"{total_percentage:.2f}%"
    )

    col4.metric(
        "Total Stocks",
        len(portfolio_df)
    )

    # Individual stock results
    st.subheader("📋 Stock-wise Performance")

    st.dataframe(
        portfolio_df.style.format({
            "Buy Price": "${:,.2f}",
            "Current Price": "${:,.2f}",
            "Investment": "${:,.2f}",
            "Current Value": "${:,.2f}",
            "Profit/Loss": "${:,.2f}",
            "Profit/Loss Percentage": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # Portfolio chart
    st.subheader("📈 Investment vs Current Value")

    chart_df = portfolio_df.set_index("Ticker")[
        ["Investment", "Current Value"]
    ]

    st.bar_chart(chart_df)

    # Download report
    st.subheader("📥 Download Your Report")

    csv_data = create_csv(portfolio_df)

    st.download_button(
        label="Download Portfolio Summary CSV",
        data=csv_data,
        file_name="portfolio_summary.csv",
        mime="text/csv",
        use_container_width=True
    )

    if total_profit_loss > 0:
        st.success("Your portfolio is currently showing a profit!")

    elif total_profit_loss < 0:
        st.warning("Your portfolio is currently showing a loss.")

    else:
        st.info("Your portfolio is currently at break-even.")

    st.caption(
        "Note: Market prices are retrieved from Yahoo Finance "
        "when available. This tracker is for informational purposes only."
    )
