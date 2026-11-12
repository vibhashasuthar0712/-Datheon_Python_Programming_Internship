# Hangman Game – Python

## Project Overview

This project is a command-line based Hangman Game developed using Python.

The game randomly selects a word from a predefined English word list, and the player has to guess the word one letter at a time before running out of attempts.

The project focuses on implementing Python programming concepts such as loops, conditional statements, functions, sets, string manipulation, and file handling.

## Objectives

- Develop an interactive word-guessing game using Python.
- Practice fundamental Python programming concepts.
- Read words from an external text file.
- Implement input validation and guessing logic.
- Track correct and incorrect guesses.
- Display the game progress after every attempt.

## Technologies Used

- Python
- Random Module
- File Handling
- Sets
- Loops and Conditional Statements
- Functions
- String Manipulation

## Project Structure

```text
01_Hangman_Game/
│
├── hangman.py
├── eng_words_list.txt
└── README.md
```

## How the Game Works

1. The game loads English words from `eng_words_list.txt`.
2. A random word is selected from the word list.
3. The selected word is displayed as hidden letters using underscores.
4. The player guesses one letter at a time.
5. If the guessed letter is correct, it is revealed in its correct position.
6. If the guessed letter is incorrect, the player loses one attempt.
7. The game displays the Hangman stages using ASCII art as incorrect guesses increase.
8. The player wins by guessing the complete word before using all attempts.
9. The game ends when the player runs out of attempts.

## Game Features

- Random word selection.
- External word list using a text file.
- Six incorrect attempts allowed.
- Interactive letter-by-letter guessing.
- ASCII Hangman stages.
- Tracking of previously guessed letters using sets.
- Display of remaining attempts.
- Win and loss messages.

## Python Concepts Implemented

### 1. File Handling
Used Python file handling to read English words from an external text file.

### 2. Random Module
Used the `random` module to select a word randomly from the available word list.

### 3. Sets
Used sets to store guessed letters and avoid processing duplicate guesses.

### 4. Loops
Used loops to continue the game until the player wins or runs out of attempts.

### 5. Conditional Statements
Used `if`, `elif`, and `else` statements to check guesses and control game outcomes.

### 6. String Manipulation
Used string operations to display correctly guessed letters in their respective positions.

## How to Run the Project

**Step 1:** Clone the repository.

```bash
git clone https://github.com/vibhashasuthar0712/Datheon_Python_Programming_Internship.git
```

**Step 2:** Navigate to the project folder.

```bash
cd Datheon_Python_Programming_Internship/01_Hangman_Game
```

**Step 3:** Run the Python program.

```bash
python hangman.py
```

**Note:** Make sure `eng_words_list.txt` is present in the same folder as `hangman.py`.

## Sample Gameplay

```text
Welcome to Hangman!

Word: _ _ _ _ _
Guess a letter: A

Correct guess!

Word: A _ _ _ _

Guess a letter: Z

Incorrect guess!
Remaining attempts: 5

Guess a letter: P

Correct guess!

Word: A P P _ _

...
```

*The sample above is illustrative; the actual word and gameplay will vary because the word is selected randomly.*

## Key Learnings

Through this project, I gained practical experience in:

- Writing structured Python programs.
- Working with external text files.
- Using built-in Python modules.
- Implementing game logic using loops and conditions.
- Managing data using sets.
- Handling user input.
- Building interactive command-line applications.

## Conclusion

The Hangman Game helped me strengthen my understanding of Python fundamentals through a practical, interactive application.

It provided hands-on experience with file handling, random selection, sets, loops, conditional logic, and user input management.

## Author

**Vibhasha Suthar**

- GitHub: https://github.com/vibhashasuthar0712
- LinkedIn: https://www.linkedin.com/in/vibhasha-suthar-280b51351/
