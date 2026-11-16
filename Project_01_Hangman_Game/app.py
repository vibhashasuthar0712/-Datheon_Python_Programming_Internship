
import streamlit as st
import random
from pathlib import Path
import string


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Hangman | Word Challenge",
    page_icon="🎯",
    layout="wide"
)


# ==========================================================
# 2. PREMIUM UI CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #E6E9FF 0%, transparent 30%),
        radial-gradient(circle at 90% 90%, #EADFFF 0%, transparent 30%),
        linear-gradient(135deg, #F8FAFF, #F1F3FF);
    color: #26324B;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.85);
    border-right: 1px solid #E8EAF5;
}

.hero {
    background: linear-gradient(120deg, #FFFFFF, #E9ECFF);
    border: 1px solid white;
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 12px 35px rgba(80,90,160,0.08);
}

.hero-tag {
    display: inline-block;
    background: #E8EBFF;
    color: #5968CE;
    border-radius: 30px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 700;
}

.hero h1 {
    color: #26345B;
    font-size: 34px;
    font-weight: 800;
    margin-top: 15px;
}

.hero p {
    color: #77819A;
    font-size: 15px;
}

.game-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid white;
    border-radius: 22px;
    padding: 25px;
    box-shadow: 0 8px 30px rgba(70,80,140,0.07);
}

.word-display {
    background: #EEF0FF;
    border-radius: 18px;
    padding: 25px 10px;
    text-align: center;
    color: #4658BD;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: 9px;
}

.section-title {
    color: #34436B;
    font-size: 19px;
    font-weight: 750;
    margin-top: 22px;
    margin-bottom: 12px;
}

div.stButton > button {
    background: rgba(255,255,255,0.9);
    color: #5365C7;
    border: 1px solid #DCE2F5;
    border-radius: 12px;
    min-height: 43px;
    font-weight: 700;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #E9EDFF;
    border-color: #929FE7;
    color: #354DB5;
    transform: translateY(-2px);
}

div.stButton > button:disabled {
    background: #E6E9F2;
    color: #A3A9B9;
    border-color: #E6E9F2;
}

.footer {
    text-align: center;
    color: #929BB0;
    font-size: 12px;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. LOAD WORD LIST
# ==========================================================

def load_words():

    file_path = Path(__file__).parent / "eng_words_list.txt"

    try:

        with open(file_path, "r", encoding="utf-8") as file:

            words = [
                word.strip().upper()
                for word in file
                if word.strip().isalpha()
            ]

        if not words:
            raise ValueError("Word list is empty.")

        return words

    except FileNotFoundError:

        st.error("eng_words_list.txt file not found!")
        st.stop()

    except OSError as error:

        st.error(f"Unable to read word list: {error}")
        st.stop()

    except ValueError as error:

        st.error(str(error))
        st.stop()


words = load_words()


# ==========================================================
# 4. HANGMAN STAGES
# ==========================================================

hangman_stages = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,

    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,

    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,

    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,

    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========
    """,

    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========
    """,

    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========
    """
]


# ==========================================================
# 5. INITIALIZE GAME
# ==========================================================

def start_new_game():

    st.session_state.secret_word = random.choice(words)

    st.session_state.guessed_letters = set()

    st.session_state.wrong_guesses = 0

    st.session_state.game_status = "playing"


if "secret_word" not in st.session_state:

    start_new_game()


# ==========================================================
# 6. GAME STATUS
# ==========================================================

secret_word = st.session_state.secret_word

guessed_letters = st.session_state.guessed_letters

wrong_guesses = st.session_state.wrong_guesses

remaining_attempts = 6 - wrong_guesses

if set(secret_word).issubset(guessed_letters):

    st.session_state.game_status = "won"

elif wrong_guesses >= 6:

    st.session_state.game_status = "lost"


# ==========================================================
# 7. SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        <h2 style="color:#5868CF;">🎯 Hangman</h2>
        <p style="color:#8992A9;font-size:12px;">
            WORD GUESSING CHALLENGE
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 📖 How to Play")

    st.markdown("""
    1. A random word is selected.
    2. Guess one letter at a time.
    3. Correct guesses reveal letters.
    4. Wrong guesses reduce your attempts.
    5. Guess the complete word before all 6 attempts are used.
    """)

    st.divider()

    st.markdown("### 🎮 Game Rules")

    st.write("❤️ Maximum mistakes: 6")

    st.write("🔤 Duplicate guesses are disabled.")

    st.write("🏆 Guess the word to win!")

    st.divider()

    if st.button(
        "🔄 Start New Game",
        use_container_width=True
    ):

        start_new_game()
        st.rerun()


# ==========================================================
# 8. HERO SECTION
# ==========================================================

st.markdown("""
<div class="hero">

    <div class="hero-tag">
        ✨ WORD GUESSING CHALLENGE
    </div>

    <h1>Let's Play Hangman! 🎯</h1>

    <p>
        Test your vocabulary and guessing skills.
        Can you discover the hidden word before
        running out of attempts?
    </p>

</div>
""", unsafe_allow_html=True)


# ==========================================================
# 9. GAME STATISTICS
# ==========================================================

st.markdown(
    '<div class="section-title">Your Game Progress</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "❤️ Attempts Left",
        remaining_attempts,
        delta=None
    )

with col2:

    st.metric(
        "❌ Wrong Guesses",
        wrong_guesses
    )

with col3:

    st.metric(
        "🔤 Letters Guessed",
        len(guessed_letters)
    )


# ==========================================================
# 10. MAIN GAME AREA
# ==========================================================

left_col, right_col = st.columns([1, 1.4])

with left_col:

    st.markdown(
        '<div class="section-title">Hangman Stage</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="game-card">
            <pre style="
                color:#4658BD;
                font-size:17px;
                font-weight:bold;
                line-height:1.4;
                text-align:center;
                background:transparent;
                border:none;
            ">{hangman_stages[wrong_guesses]}</pre>
        </div>
        """,
        unsafe_allow_html=True
    )


with right_col:

    st.markdown(
        '<div class="section-title">Guess the Hidden Word</div>',
        unsafe_allow_html=True
    )

    displayed_word = " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )

    st.markdown(
        f"""
        <div class="word-display">
            {displayed_word}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.session_state.game_status == "won":

        st.success("🎉 Congratulations! You guessed the word!")

    elif st.session_state.game_status == "lost":

        st.error(
            f"Game Over! The correct word was: {secret_word}"
        )

    else:

        st.info("💡 Choose a letter from the alphabet below.")


# ==========================================================
# 11. ALPHABET BUTTONS
# ==========================================================

st.markdown(
    '<div class="section-title">Choose Your Letter</div>',
    unsafe_allow_html=True
)

alphabet = string.ascii_uppercase

# Display letters in three rows

for row_start in range(0, len(alphabet), 9):

    letters = alphabet[row_start:row_start + 9]

    columns = st.columns(9)

    for column, letter in zip(columns, letters):

        with column:

            already_guessed = (
                letter in st.session_state.guessed_letters
            )

            game_finished = (
                st.session_state.game_status != "playing"
            )

            if st.button(
                letter,
                key=f"letter_{letter}",
                use_container_width=True,
                disabled=already_guessed or game_finished
            ):

                st.session_state.guessed_letters.add(letter)

                if letter not in st.session_state.secret_word:

                    st.session_state.wrong_guesses += 1

                # Update game status

                if set(st.session_state.secret_word).issubset(
                    st.session_state.guessed_letters
                ):

                    st.session_state.game_status = "won"

                elif st.session_state.wrong_guesses >= 6:

                    st.session_state.game_status = "lost"

                st.rerun()


# ==========================================================
# 12. GUESSED LETTERS
# ==========================================================

st.markdown(
    '<div class="section-title">Your Guessed Letters</div>',
    unsafe_allow_html=True
)

if st.session_state.guessed_letters:

    correct_letters = sorted(
        letter
        for letter in st.session_state.guessed_letters
        if letter in secret_word
    )

    incorrect_letters = sorted(
        letter
        for letter in st.session_state.guessed_letters
        if letter not in secret_word
    )

    st.write("✅ Correct:", ", ".join(correct_letters) or "None")

    st.write("❌ Incorrect:", ", ".join(incorrect_letters) or "None")

else:

    st.caption("You haven't guessed any letters yet.")


# ==========================================================
# 13. GAME RESULT AND RESTART
# ==========================================================

if st.session_state.game_status in ["won", "lost"]:

    st.divider()

    if st.session_state.game_status == "won":

        st.balloons()

        st.markdown(
            """
            <div class="hero" style="text-align:center;">
                <h1>🏆 You Won!</h1>
                <p>Excellent work! You discovered the hidden word.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="hero" style="text-align:center;">
                <h1>💔 Game Over!</h1>
                <p>Don't give up! Try another word.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button(
        "🎮 Play Again",
        use_container_width=True
    ):

        start_new_game()
        st.rerun()


# ==========================================================
# 14. FOOTER
# ==========================================================

st.markdown("""
<div class="footer">
    🎯 Hangman Word Challenge
    <br>
    Built with Python • Streamlit
    <br>
    Datheon Python Programming Internship
</div>
""", unsafe_allow_html=True)

