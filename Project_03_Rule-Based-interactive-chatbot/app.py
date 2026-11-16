
import streamlit as st

from chatbot import (
    load_faq_data,
    generate_response,
    is_exit_command
)


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Datheon | Internship Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# 2. CUSTOM CSS - PREMIUM GLASSMORPHISM
# ==========================================================

st.markdown("""
<style>

/* Main background */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #E5E9FF 0%, transparent 30%),
        radial-gradient(circle at 90% 85%, #E9DEFF 0%, transparent 30%),
        linear-gradient(135deg, #F8FAFF, #F1F4FF);
    color: #26324B;
}

/* Main container */

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.78);
    border-right: 1px solid rgba(255,255,255,0.9);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

/* Brand */

.brand {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #5266D8;
}

.brand-subtitle {
    color: #8791AA;
    font-size: 12px;
    margin-top: 3px;
}

/* Hero section */

.hero {
    background: linear-gradient(
        120deg,
        rgba(255,255,255,0.90),
        rgba(231,235,255,0.82)
    );
    border: 1px solid rgba(255,255,255,0.95);
    border-radius: 25px;
    padding: 35px;
    margin-bottom: 28px;
    box-shadow: 0 12px 40px rgba(86, 100, 170, 0.09);
    backdrop-filter: blur(18px);
}

.hero-tag {
    display: inline-block;
    background: #E8ECFF;
    color: #596AD0;
    border-radius: 30px;
    padding: 6px 13px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 15px;
}

.hero h1 {
    color: #25345B;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1.2px;
    margin: 0;
}

.hero p {
    color: #77819A;
    font-size: 15px;
    margin-top: 12px;
    line-height: 1.7;
}

/* Section headings */

.section-heading {
    color: #34436B;
    font-size: 19px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 14px;
}

/* Quick question cards */

div.stButton > button {
    background: rgba(255,255,255,0.82);
    color: #5266C9;
    border: 1px solid rgba(210,218,245,0.9);
    border-radius: 15px;
    min-height: 55px;
    font-weight: 650;
    box-shadow: 0 5px 18px rgba(83, 99, 170, 0.05);
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background: #EEF1FF;
    border-color: #9BA8ED;
    color: #4054BD;
    transform: translateY(-2px);
}

/* Chat messages */

div[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.78);
    border: 1px solid rgba(224,229,245,0.9);
    border-radius: 19px;
    padding: 14px;
    margin-bottom: 14px;
    box-shadow: 0 6px 20px rgba(65, 80, 140, 0.045);
}

/* Chat input */

div[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.9);
    border: 1px solid #DCE2F3;
    border-radius: 18px;
}

/* Sidebar text */

.sidebar-heading {
    color: #465782;
    font-size: 15px;
    font-weight: 750;
    margin-top: 20px;
    margin-bottom: 10px;
}

/* Online status */

.online-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    color: #398D70;
    background: #E9F8F1;
    padding: 7px 13px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
}

/* Footer */

.footer {
    text-align: center;
    color: #929BB0;
    font-size: 12px;
    padding: 30px 0 10px 0;
}

/* Hide default Streamlit decoration */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. LOAD FAQ DATA
# ==========================================================

@st.cache_data
def get_faq_data():
    return load_faq_data()


faq_data = get_faq_data()

if faq_data is None:

    st.error(
        "Unable to load FAQ data. "
        "Please check your sample_faq.json file."
    )

    st.stop()


# ==========================================================
# 4. SESSION STATE
# ==========================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 Welcome to Datheon Internship Support. "
                "I'm your virtual assistant. "
                "How can I help you today?"
            )
        }
    ]


if "pending_prompt" not in st.session_state:

    st.session_state.pending_prompt = None


# ==========================================================
# 5. SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">✦ Datheon</div>
        <div class="brand-subtitle">
            INTERNSHIP SUPPORT ASSISTANT
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-heading">💬 Workspace</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "＋  New Conversation",
        use_container_width=True
    ):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 Welcome back to Datheon Internship "
                    "Support. What would you like to know?"
                )
            }
        ]

        st.session_state.pending_prompt = None

        st.rerun()

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-heading">✨ Support Topics</div>',
        unsafe_allow_html=True
    )

    topics = [
        "🕒  Working Hours",
        "📁  Project Submission",
        "🏆  Certificates",
        "💻  Code Reviews",
        "📌  Internship Help"
    ]

    for topic in topics:

        st.markdown(
            f"""
            <div style="
                padding: 11px 13px;
                margin-bottom: 8px;
                border-radius: 12px;
                background: rgba(235,239,255,0.65);
                color: #596789;
                font-size: 13px;
                font-weight: 600;
            ">
                {topic}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-heading">🤖 Assistant Status</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="online-status">● Online and Ready</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            margin-top: 25px;
            color: #929BB0;
            font-size: 12px;
            line-height: 1.7;
        ">
            Your virtual internship support assistant.
            <br><br>
            Built using Python and Streamlit.
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# 6. HERO SECTION
# ==========================================================



st.html("""
<div class="hero">
    <div class="hero-tag">
        ✨ YOUR INTERNSHIP COMPANION
    </div>

    <h1>Hello, Welcome! 👋</h1>

    <p>
        Have questions about your internship?
        I'm here to help you with project submissions,
        certificates, working hours and more.
    </p>
</div>
""")




# ==========================================================
# 7. QUICK QUESTION CARDS
# ==========================================================

st.markdown(
    '<div class="section-heading">Explore Quick Help</div>',
    unsafe_allow_html=True
)

quick_questions = [
    ("🕒 Working Hours", "What are the working hours?"),
    ("🏆 Certificate", "When will I receive my certificate?"),
    ("📁 Project Submission", "How do I submit my project?"),
    ("💻 Code Review", "How does the code review work?")
]

columns = st.columns(4)

for index, (label, question) in enumerate(quick_questions):

    with columns[index]:

        if st.button(
            label,
            key=f"quick_{index}",
            use_container_width=True
        ):

            st.session_state.pending_prompt = question
            st.rerun()


# ==========================================================
# 8. CHAT SECTION
# ==========================================================

st.markdown(
    '<div class="section-heading">Your Conversation</div>',
    unsafe_allow_html=True
)

# Display previous messages

for message in st.session_state.messages:

    avatar = "🤖" if message["role"] == "assistant" else "👤"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):

        st.markdown(message["content"])


# ==========================================================
# 9. CHATBOT RESPONSE FUNCTION
# ==========================================================

def process_message(user_input):

    # Add user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Generate response

    if is_exit_command(user_input):

        response = (
            "Thank you for using Datheon Internship Support. "
            "Have a great day! 👋"
        )

    else:

        response = generate_response(
            user_input,
            faq_data
        )

    # Add assistant response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# ==========================================================
# 10. HANDLE USER INPUT
# ==========================================================

user_input = st.chat_input(
    "Ask me anything about your internship..."
)

# Handle quick question selection

if st.session_state.pending_prompt is not None:

    selected_prompt = st.session_state.pending_prompt

    st.session_state.pending_prompt = None

    process_message(selected_prompt)

    st.rerun()


# Handle normal chat input

elif user_input:

    process_message(user_input)

    st.rerun()


# ==========================================================
# 11. FOOTER
# ==========================================================

st.markdown(
    """
    <div class="footer">
        ✦ Datheon Internship Support Assistant
        <br>
        Powered by Python • Rule-Based Chatbot • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
