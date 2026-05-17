

import streamlit as st
import random
import time
from sympy import symbols, simplify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
x = symbols('x')
transformations = standard_transformations + (implicit_multiplication_application,)
# Hjælpefunktion til parsing (fixer 2x, 3x^2 osv.)
def parse_math(expr):
    expr = expr.replace("^", "**")
    return parse_expr(expr, transformations=transformations)





# ----------------------------
# HJÆLPEFUNKTIONER
# ----------------------------

def generate_derivative(level):
    if level == "Let":
        a = random.randint(1, 3)
        n = 1
    elif level == "Medium":
        a = random.randint(1, 5)
        n = random.randint(2, 3)
    else:  # Svær
        a = random.randint(2, 6)
        n = random.randint(3, 5)

    question = f"Hvad er den afledte af {a}x^{n}?"
    answer = f"{a*n}x^{n-1}"
    hint = "Brug potensreglen"
    explanation = f"{a}·{n}x^{n-1} = {a*n}x^{n-1}"

    return "Differential", question, answer, hint, explanation


def generate_integral(level):
    if level == "Let":
        a = random.randint(1, 3)
        n = 1
    elif level == "Medium":
        a = random.randint(1, 5)
        n = random.randint(1, 3)
    else:
        a = random.randint(2, 6)
        n = random.randint(2, 4)

    new_power = n + 1
    question = f"Hvad er ∫ {a}x^{n} dx?"
    answer = f"{a/new_power}x^{new_power} + C"

    hint = "Hæv eksponenten med 1 og divider"
    explanation = f"{a}/{new_power}·x^{new_power} + C"

    return "Integration", question, answer, hint, explanation

def generate_limit(level):
    if level == "Let":
        x = random.randint(1, 3)
    elif level == "Medium":
        x = random.randint(2, 5)
    else:
        x = random.randint(3, 7)

    question = f"lim x→{x} af (x^2 - {x**2})/(x - {x})"
    answer = f"{2*x}"

    hint = "Faktoriser tælleren"
    explanation = f"(x-a)(x+a)/(x-a) = x+a = {2*x}"

    return "Grænseværdi", question, answer, hint, explanation

def generate_question(level, topic_choice):
    generators = {
        "Differential": generate_derivative,
        "Integration": generate_integral,
        "Grænseværdi": generate_limit
    }

    if topic_choice != "Blandet":
        return generators[topic_choice]()

    return random.choice(list(generators.values()))()
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
if "exam_mode" not in st.session_state:
    st.session_state.exam_mode = False
# ----------------------------
# SIDEBAR
# ----------------------------


st.sidebar.title("Indstillinger")
level = st.sidebar.selectbox("Sværhedsgrad", ["Let", "Medium", "Svær"])
topic_choice = st.sidebar.selectbox("Opgavetype", ["Blandet", "Differential", "Integration", "Grænseværdi"])
num_questions = st.sidebar.slider("Antal eksamensspørgsmål", 5, 30, 10)
if st.sidebar.button("Start eksamen"):
    st.session_state.exam_mode = True
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.start_time = time.time()
    st.session_state.question = generate_question(level, topic_choice)
# ----------------------------
# UI
# ----------------------------

st.title("📘 Matematik Træner – Eksamensmode")

# Generer første opgave
if st.session_state.question is None:
    st.session_state.question = generate_question(level, topic_choice)


# Hent opgave (fix for gamle/ugyldige data i session_state)
if (st.session_state.question is None) or (len(st.session_state.question) != 5):
    st.session_state.question = generate_question(level, topic_choice)


topic, q_text, correct_answer, hint, explanation = st.session_state.question


st.subheader(topic)
st.write(q_text)

# Hint toggle
if st.button("Vis hint"):
    st.info(hint)
user_answer = st.text_input("Dit svar:")

# ----------------------------
# SVAR CHECK
# ----------------------------



if st.button("Tjek svar"):
    st.session_state.total += 1

    if not user_answer.strip():
        st.session_state.feedback = "⚠️ Skriv et svar først"
    else:
        try:
            user_expr = parse_math(user_answer)
            correct_expr = parse_math(str(correct_answer))

            st.write("DEBUG user:", user_expr)
            st.write("DEBUG correct:", correct_expr)


            if simplify(user_expr - correct_expr) == 0:
                st.session_state.score += 1
                st.session_state.feedback = "✅ Korrekt!"
            else:
                st.session_state.feedback = f"❌ Forkert. Rigtigt svar: {correct_answer}"
                st.info(f"Forklaring: {explanation}")


        except Exception:
            st.session_state.feedback = "⚠️ Kunne ikke tolke dit svar (prøv fx 2*x eller 2x)"





# ----------------------------
# NÆSTE OPGAVE
# ----------------------------

if st.button("Næste opgave"):
    st.session_state.question = generate_question(level, topic_choice)
    st.session_state.feedback = ""
    st.rerun()
# ----------------------------
# SCORE & STATISTIK
# ----------------------------

st.divider()

accuracy = (st.session_state.score / st.session_state.total * 100) if st.session_state.total else 0
st.write(f"📊 Score: {st.session_state.score} / {st.session_state.total}")
st.write(f"🎯 Accuracy: {accuracy:.1f}%")

# ----------------------------
# TIMER
# ----------------------------

elapsed = int(time.time() - st.session_state.start_time)
st.write(f"⏱ Tid: {elapsed} sekunder")

# Reset
if st.button("Reset"):
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.start_time = time.time()
    st.session_state.question = generate_question(level, topic_choice)
    st.session_state.feedback = ""
    st.session_state.exam_mode = False
