# Datheon Python Programming Internship

A collection of Python projects developed as part of the **Datheon Python Programming Internship**. This repository demonstrates practical Python programming concepts, problem-solving, data structures, file handling, input validation, and working with external data sources.

## Projects

### 1. Hangman Game

A command-line word guessing game built using Python.

**Features:**
- Random word selection from an external text file.
- Six attempts to guess the correct word.
- Dynamic display of hidden and correctly guessed letters.
- Tracks guessed and incorrect letters using Python sets.
- Prevents duplicate guesses from reducing attempts.
- ASCII-based Hangman stages.
- Input validation and win/lose messages.
- Option to play again.

**Technologies:** Python, Random Module, Sets, Loops, Functions, File Handling.

**Run the project:**

```bash
cd 01_Hangman_Game
python hangman.py
```

### 2. Investment Portfolio Tracker

A Python-based investment portfolio tracking utility that allows users to manage stock holdings and calculate their portfolio performance.

**Features:**
- Reads valid S&P 500 ticker symbols from an external CSV dataset.
- Accepts stock ticker symbols, purchase prices, and share quantities.
- Validates ticker symbols and prevents duplicate entries.
- Fetches available stock prices using Yahoo Finance through `yfinance`.
- Provides manual price entry when automatic fetching is unavailable.
- Calculates individual stock investment and current market value.
- Calculates profit/loss and percentage gain/loss for each holding.
- Calculates overall portfolio investment, current value, and performance.
- Exports stock details and portfolio summary to `portfolio_summary.csv`.

**Technologies:** Python, CSV Module, File Handling, Dictionaries, Exception Handling, yfinance.

**Install dependency:**

```bash
pip install yfinance
```

**Run the project:**

```bash
cd 02_Investment_Portfolio_Tracker
python portfolio.py
```

**Dataset:** [S&P 500 Companies CSV Dataset](https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv)

The generated `portfolio_summary.csv` contains individual stock calculations and an overall portfolio summary.

---

## Repository Structure

```text
Datheon_Python_Programming_Internship/
│
├── 01_Hangman_Game/
│   ├── hangman.py
│   └── eng_words_list.txt
│
├── 02_Investment_Portfolio_Tracker/
│   ├── portfolio.py
│   ├── constituents.csv
│   └── portfolio_summary.csv  # Generated after execution
│
├── README.md
└── .gitignore
```

## Skills & Concepts Practiced

- Python fundamentals and problem-solving
- Data structures: Lists, Sets, and Dictionaries
- Loops, conditional statements, and functions
- Input validation and exception handling
- File handling and CSV operations
- Working with external datasets
- Integrating third-party Python libraries
- Data calculations and reporting

## About This Repository

This repository documents my learning journey through practical Python programming projects during the Datheon Python Programming Internship. Each project focuses on applying programming concepts to solve real-world problems.

