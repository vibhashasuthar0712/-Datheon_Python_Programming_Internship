# Investment Portfolio Tracker – Python

## Project Overview

This project is a command-line based Investment Portfolio Tracker developed using Python.

The application allows users to manage an investment portfolio by adding stock ticker symbols, validating them against a list of S&P 500 companies, retrieving stock prices, and calculating portfolio values.

It uses a CSV file containing valid stock ticker symbols and the `yfinance` library to retrieve market price information.

The project focuses on practical Python programming concepts such as file handling, CSV operations, sets, dictionaries, input validation, exception handling, and working with external libraries.

## Objectives

- Build a simple investment portfolio tracking application.
- Validate stock ticker symbols using an external CSV file.
- Prevent duplicate stock entries.
- Retrieve the latest available stock prices.
- Calculate the total investment value of a portfolio.
- Store portfolio information in a CSV output file.
- Handle invalid inputs and price retrieval errors.

## Technologies & Libraries Used

- Python
- CSV Module
- yfinance
- Pandas
- Sets
- Dictionaries
- File Handling
- Exception Handling

## Project Structure

```text
02_Investment_Portfolio_Tracker/
│
├── portfolio.py
├── constituents.csv
├── portfolio_summary.csv
└── README.md
```

## How the Project Works

1. The application loads valid S&P 500 ticker symbols from `constituents.csv`.
2. It stores the valid ticker symbols in a Python set for efficient validation.
3. The user enters stock ticker symbols and their investment details.
4. The application checks whether each ticker is valid.
5. Duplicate ticker entries are prevented.
6. The `yfinance` library is used to retrieve the latest available stock price.
7. If the latest price is unavailable, the application attempts to use recent closing price data.
8. If automatic price retrieval fails, a manual price fallback can be used.
9. The application calculates the portfolio value using the entered investment quantities and stock prices.
10. The final portfolio summary is exported to `portfolio_summary.csv`.

## Key Features

- **Stock Ticker Validation:** Checks ticker symbols against the S&P 500 constituents list.
- **Duplicate Prevention:** Uses sets to prevent duplicate stock entries.
- **Live Price Retrieval:** Uses `yfinance` to retrieve available stock market prices.
- **Fallback Price Handling:** Attempts to use recent closing prices when the latest quote is unavailable.
- **Manual Price Fallback:** Allows manual price entry when automatic retrieval fails.
- **Portfolio Calculation:** Calculates the value of stock holdings.
- **CSV Export:** Saves portfolio details and calculated values into a CSV file.

## Python Concepts Implemented

### 1. File Handling
Used file handling to read stock ticker information from `constituents.csv` and save portfolio results.

### 2. CSV Module
Used `csv.DictReader` to read structured company data from a CSV file.

### 3. Sets
Used sets to store valid ticker symbols and efficiently check for valid and duplicate entries.

### 4. Dictionaries
Used dictionaries to organize portfolio information and store stock-related details.

### 5. Input Validation
Implemented validation to ensure that entered ticker symbols are valid and duplicate entries are avoided.

### 6. Exception Handling
Used exception handling to manage errors that may occur during stock price retrieval and user input processing.

### 7. External Library Integration
Integrated the `yfinance` library to retrieve stock market information programmatically.

## Output

The application generates a CSV file named `portfolio_summary.csv`.

The output contains portfolio information such as:

- Stock ticker symbol
- Quantity of shares
- Stock price
- Calculated investment value

The exact columns depend on the implementation in the Python script.

## How to Run the Project

**Step 1: Clone the repository**

```bash
git clone https://github.com/vibhashasuthar0712/Datheon_Python_Programming_Internship.git
```

**Step 2: Navigate to the project folder**

```bash
cd Datheon_Python_Programming_Internship/02_Investment_Portfolio_Tracker
```

**Step 3: Install the required libraries**

```bash
pip install yfinance pandas
```

**Step 4: Run the Python program**

```bash
python portfolio.py
```

**Note:** Make sure `constituents.csv` is available in the same folder as `portfolio.py`. Stock price retrieval requires an internet connection.

## Key Learnings

Through this project, I gained practical experience in:

- Reading and writing CSV files.
- Working with sets and dictionaries.
- Validating user input.
- Preventing duplicate records.
- Retrieving stock market data using an external library.
- Handling missing data and exceptions.
- Performing basic financial calculations.
- Exporting structured data into CSV files.

## Conclusion

The Investment Portfolio Tracker provided hands-on experience in developing a practical Python application that combines file handling, data validation, external library integration, and portfolio calculations.

This project strengthened my understanding of Python programming and demonstrated how Python can be used to build simple data-driven applications.

## Author

**Vibhasha Suthar**

- GitHub: https://github.com/vibhashasuthar0712
- LinkedIn: https://www.linkedin.com/in/vibhasha-suthar-280b51351/
