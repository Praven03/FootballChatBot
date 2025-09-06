import streamlit as st
import difflib
import time

# Page config
st.set_page_config(page_title="Football Q&A Chatbot", page_icon="⚽", layout="centered")

# Title
st.title("⚽ Football Q&A Chatbot")

# Store conversation history
if "history" not in st.session_state:
    st.session_state.history = []
if "last_input" not in st.session_state:
    st.session_state.last_input = ""

# Rule-based knowledge base
faq = {
    "who won the 2022 world cup": "Argentina won the 2022 FIFA World Cup in Qatar 🏆",
    "who is the goat": "Many consider Lionel Messi or Cristiano Ronaldo as the GOAT 🐐",
    "where will the 2026 world cup be held": "The 2026 World Cup will be hosted by the USA, Canada, and Mexico 🇺🇸🇨🇦🇲🇽",
    "who has the most ballon d'or": "Lionel Messi holds the record with 8 Ballon d'Or awards 🥇",
    "who has the most champions league titles": "Real Madrid has the most Champions League titles with 15 🏆",
    "which country has the most world cups": "Brazil has won the most World Cups, with 5 wins 🇧🇷",
    "who is the fastest football player": "Kylian Mbappé is often regarded as one of the fastest players ⚡",
    "who is the all time top scorer": "Cristiano Ronaldo is the all-time top scorer in football history ⚽",
    "which club does messi play for": "Lionel Messi currently plays for Inter Miami in MLS 🇺🇸",
    "who is the most expensive footballer": "Neymar’s €222 million transfer from Barcelona to PSG in 2017 remains the most expensive 💰"
}

# Example prompts
example_prompts = list(faq.keys())

st.write("💡 Example questions you can try:")
chosen_example = st.selectbox("Pick an example question:", [""] + example_prompts)

# User input (auto triggers on Enter)
user_question = st.text_input("Ask your question (press Enter):")

# Function to find best match
def get_best_answer(user_q, knowledge_base, cutoff=0.6):
    if not user_q:
        return None, None
    user_q = user_q.lower().strip()
    matches = difflib.get_close_matches(user_q, knowledge_base.keys(), n=1, cutoff=cutoff)
    if matches:
        best_match = matches[0]
        return best_match, knowledge_base[best_match]
    return None, "Sorry, I don’t know the answer to that 🤔"

# Handle input from text or dropdown
final_question = None
if user_question.strip() and user_question != st.session_state.last_input:
    final_question = user_question.strip()
    st.session_state.last_input = final_question
elif chosen_example and chosen_example != st.session_state.last_input:
    final_question = chosen_example.strip()
    st.session_state.last_input = final_question

# If there’s a new question → generate answer with typing effect
if final_question:
    matched_q, response = get_best_answer(final_question, faq)
    st.session_state.history.append(("You", final_question))

    # Typing animation
    placeholder = st.empty()
    placeholder.markdown('<div class="bot-bubble">🤖 Bot is typing...</div>', unsafe_allow_html=True)
    time.sleep(1.5)  # simulate delay
    placeholder.empty()

    st.session_state.history.append(("Bot", response))

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.history = []
    st.session_state.last_input = ""

# Scrollable + styled chat history
st.subheader("Conversation")
st.markdown(
    """
    <style>
    .chat-history {
        max-height: 350px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    .user-bubble {
        background-color: #0078ff;
        color: white;
        padding: 8px 12px;
        border-radius: 15px;
        margin: 5px 0;
        text-align: right;
        display: inline-block;
        max-width: 80%;
    }
    .bot-bubble {
        background-color: #e5e5ea;
        color: black;
        padding: 8px 12px;
        border-radius: 15px;
        margin: 5px 0;
        text-align: left;
        display: inline-block;
        max-width: 80%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="chat-history">', unsafe_allow_html=True)
for speaker, text in st.session_state.history:
    if speaker == "You":
        st.markdown(f'<div class="user-bubble">👤 {text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">🤖 {text}</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
