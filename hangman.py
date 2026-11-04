
import random

with open("eng_words_list.txt", "r") as file:
    words = file.readlines()


# Hangman stages
hangman_stages = [

    # Stage 0: Empty gallows
    """
     +---+
     |   |
         |
         |
         |
    =========
    """,

    # Stage 1: Head
    """
     +---+
     |   |
     O   |
         |
         |
    =========
    """,

    # Stage 2: Body
    """
     +---+
     |   |
     O   |
     |   |
         |
    =========
    """,

    # Stage 3: Left arm
    """
     +---+
     |   |
     O   |
    /|   |
         |
    =========
    """,

    # Stage 4: Right arm
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    =========
    """,

    # Stage 5: Left leg
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    =========
    """,

    # Stage 6: Right leg
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    =========
    """
]


def play_game():

    word = random.choice(words).strip().lower()
    attempts = 6

    guessed_letters = set()
    wrong_letters = set()

    display = ["_"] * len(word)

    # Show initial gallows
    print(hangman_stages[0])

    while attempts > 0 and "_" in display:

        guess = input("Enter a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single alphabet only!")
            continue

        if guess in guessed_letters or guess in wrong_letters:
            print("You already guessed this letter!")

        elif guess in word:
            guessed_letters.add(guess)
            print("You guessed a correct letter!")

        else:
            wrong_letters.add(guess)
            attempts -= 1

            print("You guessed a wrong letter!")
            print("Now you have", attempts, "attempts left")

            wrong_count = 6 - attempts
            print(hangman_stages[wrong_count])

        # Update hidden word display
        display = []

        for letter in word:
            if letter in guessed_letters:
                display.append(letter)
            else:
                display.append("_")

        print(" ".join(display))

    # Win or Lose condition
    if "_" not in display:
        print("Congratulations! You won!")

    else:
        print("Game Over! You lost!")
        print("The correct word was:", word)


# Play Again feature
while True:

    play_game()

    choice = input("Do you want to play again? (yes/no): ").lower().strip()

    if choice != "yes":
        print("Thanks for playing!")
        break
