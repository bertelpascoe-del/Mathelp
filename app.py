import streamlit as st
import random

# Opgaver
questions = [
    {
        "topic": "Grænseværdi",
        "q": "lim x→2 af (x^2 - 4)/(x - 2)",
        "a": "4"
    },
    {
        "topic": "Differential",
        "q": "Hvad er den afledte af f(x) = x^2?",
        "a": "2x"
    },
    {
        "topic": "Integration",
        "q": "Hvad er ∫ 2x dx?",
        "a": "x^2 + C"
    }
]
# Session state setup
if "index" not in st.session_state:
    st.session_state.index = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
# Funktioner

def next_question():
    st.session_state.index = (st.session_state.index + 1) % len(questions)
    st.session_state.feedback = ""

# UI
st.title("📘 Matematik Træner")

q = questions[st.session_state.index]


st.subheader(q["topic"])
st.write(q["q"])


user_answer = st.text_input("Dit svar:")


if st.button("Tjek svar"):
    if user_answer.strip().lower() == q["a"].lower():
        st.session_state.feedback = "✅ Korrekt!"
    else:
        st.session_state.feedback = f"❌ Forkert. Rigtigt svar: {q['a']}"

if st.session_state.feedback:
    st.write(st.session_state.feedback)

if st.button("Næste opgave"):
    next_question()

# Ekstra: Random opgave
if st.button("Tilfældig opgave"):
    st.session_state.index = random.randint(0, len(questions) - 1)
    st.session_state.feedback = ""
