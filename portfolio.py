import csv
import math
import yfinance as yf


# Function to fetch the latest available stock price
def fetch_stock_price(ticker):

    # Convert ticker format for Yahoo Finance
    yahoo_ticker = ticker.replace(".", "-")

    stock = yf.Ticker(yahoo_ticker)

    # First attempt: Fetch the latest available quote
    try:
        price = stock.fast_info["last_price"]

        price = float(price)

        if math.isfinite(price) and price > 0:
            return price, "Yahoo Finance Quote"

    except Exception:
        pass

    # Second attempt: Fetch the latest available closing price
    try:
        history = stock.history(period="5d")

        if not history.empty:

            closing_prices = history["Close"].dropna()

            if not closing_prices.empty:

                price = float(closing_prices.iloc[-1])

                if math.isfinite(price) and price > 0:
                    return price, "Latest Available Closing Price"

    except Exception:
        pass

    # If both attempts fail
    raise ValueError("Stock price is unavailable.")


# Function to validate positive float values
def get_positive_float(message):

    while True:

        try:
            value = float(input(message))

            if math.isfinite(value) and value > 0:
                return value

            else:
                print("Value must be greater than zero. Please try again.")

        except ValueError:
            print("Invalid input! Please enter a valid number.")


# Function to validate positive integer values
def get_positive_integer(message):

    while True:

        try:
            value = int(input(message))

            if value > 0:
                return value

            else:
                print("Value must be a positive integer. Please try again.")

        except ValueError:
            print("Invalid input! Please enter a whole number.")


# --------------------------------------------------
# STEP 1: Read valid S&P 500 ticker symbols from CSV
# --------------------------------------------------

valid_tickers = set()

with open(
    "constituents.csv",
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        ticker = row["Symbol"].strip().upper()

        valid_tickers.add(ticker)


print("Total valid tickers:", len(valid_tickers))


# --------------------------------------------------
# STEP 2: Create an empty dictionary for portfolio
# --------------------------------------------------

portfolio = {}


# Ask user how many stocks they want to add
total_stocks = get_positive_integer(
    "\nHow many stocks do you want to add? "
)


# --------------------------------------------------
# STEP 3: Take stock details from the user
# --------------------------------------------------

for i in range(total_stocks):

    print(f"\n========== STOCK {i + 1} ==========")

    # Validate ticker symbol
    while True:

        ticker = input(
            "Enter stock ticker: "
        ).strip().upper()

        if ticker in portfolio:

            print(
                "Ticker already exists in the portfolio! "
                "Please enter a different ticker."
            )

        elif ticker not in valid_tickers:

            print("Invalid ticker! Please try again.")

        else:
            break


    # Get buy price
    buy_price = get_positive_float(
        "Enter the buy price: "
    )


    # Get quantity
    quantity = get_positive_integer(
        "Enter the quantity of stocks: "
    )


    # --------------------------------------------------
    # STEP 4: Fetch current stock price automatically
    # --------------------------------------------------

    print(f"\nFetching market price for {ticker}...")

    try:

        current_price, price_source = fetch_stock_price(ticker)

        print(f"Latest available price: ${current_price:.2f}")
        print(f"Price source: {price_source}")

    except Exception as error:

        print(f"Unable to fetch stock price: {error}")

        print("You can enter the price manually instead.")

        current_price = get_positive_float(
            "Enter the current stock price manually: "
        )

        price_source = "Manual Entry"


    # Store stock details in nested dictionary
    portfolio[ticker] = {

        "buy_price": buy_price,
        "quantity": quantity,
        "current_price": current_price,
        "price_source": price_source

    }


# --------------------------------------------------
# STEP 5: Initialize portfolio totals
# --------------------------------------------------

total_investment = 0
total_current_value = 0
total_portfolio_profit_loss = 0


print("\n========== PORTFOLIO SUMMARY ==========\n")


# --------------------------------------------------
# STEP 6: Calculate individual stock values
# --------------------------------------------------

for ticker, data in portfolio.items():

    # Calculate total investment
    investment = data["buy_price"] * data["quantity"]

    # Calculate current market value
    current_value = data["current_price"] * data["quantity"]

    # Calculate profit or loss
    profit_loss = current_value - investment

    # Calculate profit/loss percentage
    profit_loss_percentage = (
        profit_loss / investment
    ) * 100


    # Add individual values to portfolio totals
    total_investment += investment

    total_current_value += current_value

    total_portfolio_profit_loss += profit_loss


    # Display individual stock summary
    print(f"Stock: {ticker}")

    print(f"Buy Price: ${data['buy_price']:.2f}")

    print(f"Quantity: {data['quantity']}")

    print(f"Current Price: ${data['current_price']:.2f}")

    print(f"Investment: ${investment:.2f}")

    print(f"Current Value: ${current_value:.2f}")

    print(f"Profit/Loss: ${profit_loss:+.2f}")

    print(
        f"Profit/Loss Percentage: "
        f"{profit_loss_percentage:+.2f}%"
    )

    print("---------------------------------------")


# --------------------------------------------------
# STEP 7: Calculate overall portfolio performance
# --------------------------------------------------

if total_investment > 0:

    total_portfolio_profit_loss_percentage = (
        total_portfolio_profit_loss / total_investment
    ) * 100

else:

    total_portfolio_profit_loss_percentage = 0


# --------------------------------------------------
# STEP 8: Display total portfolio summary
# --------------------------------------------------

print("\n========== TOTAL PORTFOLIO ==========")

print(f"Total Investment: ${total_investment:.2f}")

print(f"Total Current Value: ${total_current_value:.2f}")

print(
    f"Total Profit/Loss: "
    f"${total_portfolio_profit_loss:+.2f}"
)

print(
    f"Total Profit/Loss Percentage: "
    f"{total_portfolio_profit_loss_percentage:+.2f}%"
)


# --------------------------------------------------
# STEP 9: Export portfolio details to CSV
# --------------------------------------------------

with open(
    "portfolio_summary.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    # Create CSV writer object
    writer = csv.writer(file)


    # Write column headings
    writer.writerow([

        "Ticker",
        "Buy Price",
        "Quantity",
        "Current Price",
        "Price Source",
        "Investment",
        "Current Value",
        "Profit/Loss",
        "Profit/Loss Percentage"

    ])


    # Write individual stock details
    for ticker, data in portfolio.items():

        investment = (
            data["buy_price"] * data["quantity"]
        )

        current_value = (
            data["current_price"] * data["quantity"]
        )

        profit_loss = current_value - investment

        profit_loss_percentage = (
            profit_loss / investment
        ) * 100


        writer.writerow([

            ticker,
            data["buy_price"],
            data["quantity"],
            data["current_price"],
            data["price_source"],
            round(investment, 2),
            round(current_value, 2),
            round(profit_loss, 2),
            round(profit_loss_percentage, 2)

        ])


    # Write overall portfolio summary row
    writer.writerow([

        "TOTAL",
        "",
        "",
        "",
        "",
        round(total_investment, 2),
        round(total_current_value, 2),
        round(total_portfolio_profit_loss, 2),
        round(total_portfolio_profit_loss_percentage, 2)

    ])


print(
    "\nPortfolio summary successfully saved "
    "to portfolio_summary.csv!"
)