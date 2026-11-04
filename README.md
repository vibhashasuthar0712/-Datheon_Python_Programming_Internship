# Datheon Python Programming Internship

This repository contains Python programming projects and assignments completed as part of the Datheon Python Programming Internship.

## Project 1: Hangman Game

A terminal-based Hangman game developed using Python. The player must guess a randomly selected hidden word, one letter at a time, within six incorrect attempts.

### Features

- Random word selection using Python's `random` module.
- English word dataset loaded from a text file.
- Interactive letter-by-letter guessing.
- Masked word display.
- Tracks correctly and incorrectly guessed letters using sets.
- Prevents duplicate guesses from reducing attempts.
- Six attempts with progressive ASCII Hangman drawings.
- Input validation.
- Win and lose messages.
- Reveals the correct word when the player loses.
- Play Again functionality.

### Technologies Used

- Python 3
- Random module
- File Handling
- Lists and Sets
- Loops and Conditional Statements
- Functions

### Project Structure

```text
01_Hangman_Game/
├── hangman.py
└── eng_words_list.txt
```

### How to Run

1. Install Python 3.
2. Clone or download this repository.
3. Open the project folder in VS Code or any Python IDE.
4. Navigate to `01_Hangman_Game`.
5. Run the following command:

```bash
python hangman.py
```

### Dataset Source

English word list: [Google 10,000 English Words](https://github.com/first20hours/google-10000-english)

### Learning Outcome

This project helped me practice Python fundamentals, including file handling, random selection, data structures, loops, functions, input validation, and conditional logic.

---

**Author:** Vibhasha Suthar  
**Internship:** Datheon Python Programming Internship
