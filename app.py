import streamlit as st
import random
import time
# ----------------------------
# HJÆLPEFUNKTIONER
# ----------------------------


def generate_derivative():
    a = random.randint(1, 5)
    n = random.randint(1, 4)
    question = f"Hvad er den afledte af {a}x^{n}?"
    answer = f"{a*n}x^{n-1}"
    return "Differential", question, answer




def generate_integral():
    a = random.randint(1, 5)
    n = random.randint(1, 4)
    question = f"Hvad er ∫ {a}x^{n} dx?"
    new_power = n + 1
    answer = f"{a/new_power}x^{new_power} + C"
    return "Integration", question, answer




def generate_limit():
    x = random.randint(1, 5)
    question = f"lim x→{x} af (x^2 - {x**2})/(x - {x})"
    answer = f"{2*x}"
    return "Grænseværdi", question, answer




def generate_question(level):
    if level == "Let":
        return random.choice([
            generate_derivative(),
            generate_integral()
        ])
    elif level == "Medium":
        return random.choice([
            generate_derivative(),
            generate_integral(),
            generate_limit()
        ])
    else:
        return random.choice([
            generate_derivative(),
            generate_integral(),
            generate_limit()
        ])


# ----------------------------
# SESSION STATE
# ----------------------------


if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "question" not in st.session_state:
    st.session_state.question = None
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
# ----------------------------
# UI
# ----------------------------
st.title("📘 Matematik Træner – Eksamensmode")
level = st.selectbox("Vælg sværhedsgrad", ["Let", "Medium", "Svær"])
# Generer første opgave
if st.session_state.question is None:
    st.session_state.question = generate_question(level)
# Hent opgave
topic, q_text, correct_answer = st.session_state.question
st.subheader(topic)
st.write(q_text)


user_answer = st.text_input("Dit svar:")

# ----------------------------
# SVAR CHECK
# ----------------------------
if st.button("Tjek svar"):
    st.session_state.total += 1


    if user_answer.strip().lower() == str(correct_answer).lower():
        st.session_state.score += 1
        st.session_state.feedback = "✅ Korrekt!"
    else:
        st.session_state.feedback = f"❌ Forkert. Rigtigt svar: {correct_answer}"
# Feedback
if st.session_state.feedback:
    st.write(st.session_state.feedback)

# ----------------------------
# NÆSTE OPGAVE
# ----------------------------


if st.button("Næste opgave"):
    st.session_state.question = generate_question(level)
    st.session_state.feedback = ""
# ----------------------------
# SCORE & STATISTIK
# ----------------------------


st.divider()


if st.session_state.total > 0:
    accuracy = st.session_state.score / st.session_state.total * 100
else:
    accuracy = 0


st.write(f"📊 Score: {st.session_state.score} / {st.session_state.total}")
st.write(f"🎯 Accuracy: {accuracy:.1f}%")


# ----------------------------
# TIMER
# ----------------------------


elapsed = int(time.time() - st.session_state.start_time)
st.write(f"⏱ Tid: {elapsed} sekunder")


# Reset knap
if st.button("Reset"):
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.start_time = time.time()
    st.session_state.question = generate_question(level)
    st.session_state.feedback = ""
