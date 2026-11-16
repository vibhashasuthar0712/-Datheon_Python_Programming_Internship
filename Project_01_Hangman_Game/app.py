
import random
import string
from pathlib import Path

import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hangman | Word Challenge",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. PREMIUM LIGHT UI CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 8% 8%, #e7eaff 0%, transparent 28%),
            radial-gradient(circle at 92% 88%, #efe6ff 0%, transparent 30%),
            linear-gradient(135deg, #f9faff 0%, #f1f3ff 100%);
        color: #26324b;
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2rem;
        padding-bottom: 1rem;
    }

    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.92);
        border-right: 1px solid #e6e9f5;
    }

    .hero {
        background: linear-gradient(120deg, #ffffff, #e9edff);
        border: 1px solid white;
        border-radius: 24px;
        padding: 30px 34px;
        margin-bottom: 22px;
        box-shadow: 0 12px 35px rgba(80, 90, 160, 0.09);
    }

    .hero-tag {
        display: inline-block;
        background: #e8ebff;
        color: #5968ce;
        border-radius: 30px;
        padding: 7px 14px;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.7px;
    }

    .hero h1 {
        color: #26345b;
        font-size: clamp(28px, 4vw, 38px);
        font-weight: 800;
        margin: 15px 0 8px 0;
    }

    .hero p {
        color: #77819a;
        font-size: 15px;
        margin-bottom: 0;
        line-height: 1.6;
    }

    .section-title {
        color: #34436b;
        font-size: 19px;
        font-weight: 750;
        margin: 18px 0 12px 0;
    }

    .game-card {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid white;
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 8px 30px rgba(70, 80, 140, 0.07);
        min-height: 245px;
    }

    .hangman-art {
        color: #4658bd;
        font-size: 19px;
        font-weight: bold;
        line-height: 1.5;
        text-align: center;
        white-space: pre;
        overflow-x: auto;
        margin: 0;
        padding: 15px 0;
        background: transparent;
    }

    .word-display {
        background: #eef0ff;
        border: 1px solid #e1e5ff;
        border-radius: 18px;
        padding: 25px 12px;
        text-align: center;
        color: #4658bd;
        font-size: clamp(23px, 3vw, 34px);
        font-weight: 800;
        letter-spacing: 7px;
        overflow-wrap: anywhere;
    }

    .word-info {
        text-align: center;
        color: #8992a9;
        font-size: 13px;
        margin-top: 12px;
    }

    .guess-card {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid #edf0fa;
        border-radius: 16px;
        padding: 16px;
        min-height: 85px;
        box-shadow: 0 5px 18px rgba(70, 80, 140, 0.04);
    }

    .guess-label {
        font-size: 13px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .guess-value {
        font-size: 16px;
        font-weight: 700;
        overflow-wrap: anywhere;
    }

    div.stButton > button {
        background: rgba(255, 255, 255, 0.95);
        color: #5365c7;
        border: 1px solid #dce2f5;
        border-radius: 12px;
        min-height: 42px;
        font-weight: 750;
        transition: all 0.18s ease;
    }

    div.stButton > button:hover:not(:disabled) {
        background: #e9edff;
        border-color: #929fe7;
        color: #354db5;
        transform: translateY(-2px);
    }

    div.stButton > button:disabled {
        background: #e9ebf2;
        color: #a3a9b9;
        border-color: #e6e9f2;
        opacity: 0.8;
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid #edf0fa;
        border-radius: 16px;
        padding: 14px 16px;
        box-shadow: 0 5px 18px rgba(70, 80, 140, 0.04);
    }

    .footer {
        text-align: center;
        color: #929bb0;
        font-size: 12px;
        padding: 24px 0 8px 0;
        line-height: 1.8;
    }

    @media (max-width: 700px) {
        .hero {
            padding: 22px;
        }

        .word-display {
            letter-spacing: 4px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. LOAD WORD LIST
# ============================================================

def load_words():

    file_path = Path(__file__).parent / "eng_words_list.txt"

    try:
        with file_path.open("r", encoding="utf-8") as file:

            valid_words = [
                line.strip().upper()
                for line in file
                if line.strip().isalpha()
            ]

        if not valid_words:
            st.error(
                "The word list is empty. "
                "Add words to eng_words_list.txt."
            )
            st.stop()

        return valid_words

    except FileNotFoundError:
        st.error(
            "eng_words_list.txt was not found. "
            "Keep it in the same folder as app.py."
        )
        st.stop()

    except OSError as error:
        st.error(f"Unable to read the word list: {error}")
        st.stop()


WORDS = load_words()


# ============================================================
# 4. HANGMAN DRAWING STAGES
# ============================================================

HANGMAN_STAGES = [

    # Stage 0: No wrong guesses
    r"""
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,

    # Stage 1: Head
    r"""
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,

    # Stage 2: Body
    r"""
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,

    # Stage 3: Left arm
    r"""
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,

    # Stage 4: Right arm
    r"""
      +---+
      |   |
      O   |
     /|\  |
          |
          |
    =========
    """,

    # Stage 5: Left leg
    r"""
      +---+
      |   |
      O   |
     /|\  |
     /    |
          |
    =========
    """,

    # Stage 6: Right leg
    r"""
      +---+
      |   |
      O   |
     /|\  |
     / \  |
          |
    =========
    """
]


# ============================================================
# 5. INITIALIZE NEW GAME
# ============================================================

def start_new_game():

    previous_word = st.session_state.get("secret_word")

    # Avoid repeating the previous word if possible
    if len(WORDS) > 1:

        choices = [
            word for word in WORDS
            if word != previous_word
        ]

        secret_word = random.choice(choices)

    else:
        secret_word = WORDS[0]

    st.session_state.secret_word = secret_word
    st.session_state.guessed_letters = set()
    st.session_state.wrong_guesses = 0
    st.session_state.game_status = "playing"


if "secret_word" not in st.session_state:
    start_new_game()


# ============================================================
# 6. PROCESS USER GUESS
# ============================================================

def process_guess(letter):

    if st.session_state.game_status != "playing":
        return

    if letter in st.session_state.guessed_letters:
        return

    # Store guessed letter
    st.session_state.guessed_letters.add(letter)

    # Increase wrong guesses only for incorrect letters
    if letter not in st.session_state.secret_word:
        st.session_state.wrong_guesses += 1

    # Check win condition
    if set(st.session_state.secret_word).issubset(
        st.session_state.guessed_letters
    ):
        st.session_state.game_status = "won"

    # Check lose condition
    elif st.session_state.wrong_guesses >= 6:
        st.session_state.game_status = "lost"


# ============================================================
# 7. CURRENT GAME VALUES
# ============================================================

secret_word = st.session_state.secret_word
guessed_letters = st.session_state.guessed_letters
wrong_guesses = st.session_state.wrong_guesses

remaining_attempts = max(0, 6 - wrong_guesses)
game_status = st.session_state.game_status

stage_index = min(
    wrong_guesses,
    len(HANGMAN_STAGES) - 1
)


# ============================================================
# 8. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <h2 style="color:#5868CF; margin-bottom:0;">
            🎯 Hangman
        </h2>

        <p style="color:#8992A9; font-size:12px;">
            WORD GUESSING CHALLENGE
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 📖 How to Play")

    st.markdown(
        """
        1. A random word is selected.
        2. Guess one letter at a time.
        3. Correct guesses reveal letters.
        4. Wrong guesses add one body part.
        5. Find the word before all 6 attempts are used.
        """
    )

    st.divider()

    st.markdown("### 🎮 Game Rules")

    st.write("❤️ Maximum mistakes: 6")
    st.write("🔤 Duplicate guesses are disabled.")
    st.write("🏆 Guess the complete word to win!")

    st.divider()

    if st.button(
        "🔄 Start New Game",
        use_container_width=True
    ):
        start_new_game()
        st.rerun()


# ============================================================
# 9. HERO SECTION
# ============================================================
st.html("""
<div style="
    background: linear-gradient(120deg, #ffffff, #e9edff);
    border: 1px solid white;
    border-radius: 24px;
    padding: 30px 34px;
    margin-bottom: 22px;
    box-shadow: 0 12px 35px rgba(80,90,160,0.09);
">

    <div style="
        display: inline-block;
        background: #e8ebff;
        color: #5968ce;
        border-radius: 30px;
        padding: 7px 14px;
        font-size: 12px;
        font-weight: 800;
    ">
        ✨ WORD GUESSING CHALLENGE
    </div>

    <h1 style="
        color: #26345b;
        font-size: 36px;
        margin: 15px 0 8px;
    ">
        Let's Play Hangman! 🎯
    </h1>

    <p style="
        color: #77819a;
        font-size: 15px;
        line-height: 1.6;
        margin: 0;
    ">
        Test your vocabulary and guessing skills.
        Can you discover the hidden word before
        running out of attempts?
    </p>

</div>
""")


# ============================================================
# 10. GAME STATISTICS
# ============================================================

st.markdown(
    '<div class="section-title">Your Game Progress</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "❤️ Attempts Left",
        remaining_attempts
    )

with col2:
    st.metric(
        "❌ Wrong Guesses",
        f"{wrong_guesses}/6"
    )

with col3:
    st.metric(
        "🔤 Letters Guessed",
        len(guessed_letters)
    )


# ============================================================
# 11. MAIN GAME AREA
# ============================================================

left_col, right_col = st.columns(
    [1, 1.35],
    gap="large"
)


# ----------------------------
# LEFT SIDE: HANGMAN DRAWING
# ----------------------------

with left_col:

    st.markdown(
        '<div class="section-title">Hangman Stage</div>',
        unsafe_allow_html=True
    )

    st.html(f"""
    <div style="
        background: rgba(255,255,255,0.92);
        border: 1px solid white;
        border-radius: 22px;
        padding: 22px;
        min-height: 245px;
        box-shadow: 0 8px 30px rgba(70,80,140,0.07);
        display: flex;
        justify-content: center;
        align-items: center;
    ">
        <pre style="
            color: #4658BD;
            font-size: 19px;
            font-weight: bold;
            line-height: 1.5;
            text-align: center;
            white-space: pre;
            margin: 0;
            background: transparent;
            border: none;
        ">{HANGMAN_STAGES[stage_index]}</pre>
    </div>
    """)

    if wrong_guesses == 0:
        st.caption("You are safe. Keep guessing!")

    elif remaining_attempts > 0:
        st.caption(
            f"Careful! You have {remaining_attempts} attempts remaining."
        )

    else:
        st.caption("No attempts left.")

with right_col:

    st.markdown(
        '<div class="section-title">Discover the Hidden Word</div>',
        unsafe_allow_html=True
    )

    # Show blanks and reveal correctly guessed letters
    display_word = " ".join(
        letter if letter in st.session_state.guessed_letters else "_"
        for letter in st.session_state.secret_word
    )

    # Reveal complete word only when the player loses
    if st.session_state.game_status == "lost":
        display_word = " ".join(st.session_state.secret_word)

    st.html(f"""
    <div style="
        background: #eef0ff;
        border: 1px solid #e1e5ff;
        border-radius: 18px;
        padding: 25px 12px;
        text-align: center;
        color: #4658bd;
        font-size: 30px;
        font-weight: 800;
        letter-spacing: 7px;
    ">
        {display_word}
    </div>

    <div style="
        text-align: center;
        color: #8992a9;
        font-size: 13px;
        margin-top: 12px;
    ">
        🔤 Word Length: {len(st.session_state.secret_word)} Letters
    </div>
    """)

    st.write("")

    if st.session_state.game_status == "playing":
        st.info("Choose a letter below to reveal the hidden word.")

    elif st.session_state.game_status == "won":
        st.success("You successfully guessed the word!")

    else:
        st.error(f"The correct word was: {secret_word}")


# ============================================================
# 12. ALPHABET BUTTONS
# ============================================================

st.markdown(
    '<div class="section-title">Choose Your Letter</div>',
    unsafe_allow_html=True
)

alphabet = string.ascii_uppercase

# Display alphabet in three rows
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
                key=f"guess_{letter}",
                use_container_width=True,
                disabled=already_guessed or game_finished
            ):

                process_guess(letter)
                st.rerun()


# ============================================================
# 13. GUESSED LETTERS
# ============================================================

st.markdown(
    '<div class="section-title">Your Guessed Letters</div>',
    unsafe_allow_html=True
)

correct_letters = sorted(
    letter for letter in st.session_state.guessed_letters
    if letter in st.session_state.secret_word
)

incorrect_letters = sorted(
    letter for letter in st.session_state.guessed_letters
    if letter not in st.session_state.secret_word
)

correct_col, incorrect_col = st.columns(2)

with correct_col:

    correct_display = ", ".join(correct_letters) if correct_letters else "None yet"

    st.html(f"""
    <div style="
        background: white;
        border: 1px solid #e5f3eb;
        border-radius: 16px;
        padding: 18px;
        min-height: 90px;
    ">
        <div style="color:#27966B; font-weight:750; margin-bottom:10px;">
            ✅ Correct Letters
        </div>
        <div style="color:#27966B; font-size:17px; font-weight:700;">
            {correct_display}
        </div>
    </div>
    """)

with incorrect_col:

    incorrect_display = ", ".join(incorrect_letters) if incorrect_letters else "None yet"

    st.html(f"""
    <div style="
        background: white;
        border: 1px solid #f5e5e7;
        border-radius: 16px;
        padding: 18px;
        min-height: 90px;
    ">
        <div style="color:#D45C68; font-weight:750; margin-bottom:10px;">
            ❌ Incorrect Letters
        </div>
        <div style="color:#D45C68; font-size:17px; font-weight:700;">
            {incorrect_display}
        </div>
    </div>
    """)

if not st.session_state.guessed_letters:
    st.caption("You haven't guessed any letters yet. Start guessing!")

# ============================================================
# 14. GAME RESULT
# ============================================================

if st.session_state.game_status in ["won", "lost"]:

    st.divider()

    if st.session_state.game_status == "won":

        st.balloons()

        st.markdown(
            """
            <div class="hero" style="text-align:center;">
                <h1>🏆 You Won!</h1>
                <p>
                    Excellent work!
                    You discovered the hidden word.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="hero" style="text-align:center;">
                <h1>💔 Game Over!</h1>
                <p>
                    Don't give up!
                    Try another word.
                </p>
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


# ============================================================
# 15. FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🎯 Hangman Word Challenge<br>
        Built with Python • Streamlit<br>
        Datheon Python Programming Internship
    </div>
    """,
    unsafe_allow_html=True
)
