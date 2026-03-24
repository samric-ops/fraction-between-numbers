import streamlit as st
import random
from fractions import Fraction
from datetime import datetime

# ---------- Helper functions ----------
def generate_question_pair():
    """Generate two distinct rational numbers."""
    # Generate two random rationals between 0 and 10
    # Using simple integers for denominators to keep numbers readable
    a = Fraction(random.randint(1, 20), random.randint(1, 10))
    b = Fraction(random.randint(1, 20), random.randint(1, 10))
    while a == b:  # ensure distinct
        b = Fraction(random.randint(1, 20), random.randint(1, 10))
    return (a, b) if a < b else (b, a)  # return sorted (smaller, larger)

def fraction_to_str(frac):
    """Pretty print a fraction, e.g., '3/4'."""
    if frac.denominator == 1:
        return str(frac.numerator)
    return f"{frac.numerator}/{frac.denominator}"

def is_between(num, a, b):
    """Check if num is strictly between a and b."""
    return a < num < b

def correct_fraction(a, b):
    """Return a fraction strictly between a and b (the average)."""
    return (a + b) / 2

# ---------- Session state initialisation ----------
if 'questions' not in st.session_state:
    st.session_state.questions = [generate_question_pair() for _ in range(15)]
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'student_answers' not in st.session_state:
    st.session_state.student_answers = ["" for _ in range(15)]
if 'results' not in st.session_state:
    st.session_state.results = None

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Fraction Between Two Numbers - Quiz", page_icon="🧮")
st.title("🧮 Fraction Between Two Numbers - 15‑Item Quiz")
st.markdown("For each question, write a **fraction (or decimal)** that lies **strictly between** the two given numbers.")

# ---------- Student Information ----------
st.subheader("Student Information")
col1, col2, col3 = st.columns(3)
with col1:
    surname = st.text_input("Surname *", key="surname")
with col2:
    first_name = st.text_input("First Name *", key="first_name")
with col3:
    middle_initial = st.text_input("Middle Initial (optional)", max_chars=1, key="middle")

# ---------- Button to Regenerate Questions ----------
if st.button("🔄 Regenerate Questions"):
    st.session_state.questions = [generate_question_pair() for _ in range(15)]
    st.session_state.submitted = False
    st.session_state.student_answers = ["" for _ in range(15)]
    st.session_state.results = None
    st.rerun()

# ---------- Display Questions ----------
st.subheader("Questions")
with st.form("quiz_form"):
    for i, (low, high) in enumerate(st.session_state.questions):
        st.markdown(f"**Q{i+1}:**  {fraction_to_str(low)}  and  {fraction_to_str(high)}")
        student_input = st.text_input(
            "Your answer",
            key=f"ans_{i}",
            value=st.session_state.student_answers[i] if not st.session_state.submitted else st.session_state.student_answers[i],
            disabled=st.session_state.submitted  # disable after submission
        )
        # Store answer in session state as user types (only if not submitted)
        if not st.session_state.submitted:
            st.session_state.student_answers[i] = student_input
    submitted = st.form_submit_button("✅ Submit Answers")

# ---------- Process Submission ----------
if submitted:
    if not surname or not first_name:
        st.error("Please fill in Surname and First Name.")
    else:
        results = []
        all_correct = True
        for i, (low, high) in enumerate(st.session_state.questions):
            answer_str = st.session_state.student_answers[i].strip()
            if not answer_str:
                results.append((False, "No answer", None))
                all_correct = False
                continue
            try:
                student_frac = Fraction(answer_str)
                correct = is_between(student_frac, low, high)
                if correct:
                    results.append((True, student_frac, None))
                else:
                    correct_example = correct_fraction(low, high)
                    results.append((False, student_frac, correct_example))
                    all_correct = False
            except Exception:
                results.append((False, "Invalid input", None))
                all_correct = False
        st.session_state.results = results
        st.session_state.submitted = True

# ---------- Display Results After Submission ----------
if st.session_state.submitted and st.session_state.results is not None:
    st.subheader("Results")
    for i, (low, high) in enumerate(st.session_state.questions):
        correct, student_ans, correct_example = st.session_state.results[i]
        if correct:
            st.success(f"✅ Q{i+1}: {student_ans} is between {fraction_to_str(low)} and {fraction_to_str(high)}")
        else:
            if student_ans == "Invalid input":
                st.error(f"❌ Q{i+1}: Invalid input. A valid fraction between {fraction_to_str(low)} and {fraction_to_str(high)} would be {fraction_to_str(correct_example)}.")
            else:
                st.error(f"❌ Q{i+1}: {student_ans} is NOT between {fraction_to_str(low)} and {fraction_to_str(high)}. Example correct fraction: {fraction_to_str(correct_example)}")

    # ---------- Download Report ----------
    full_name = f"{surname} {first_name} {middle_initial}".strip() if middle_initial else f"{surname} {first_name}".strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"STUDENT OUTPUT - FRACTION BETWEEN TWO NUMBERS QUIZ\n"
    report += f"Student: {full_name}\n"
    report += f"Date: {timestamp}\n\n"
    for i, (low, high) in enumerate(st.session_state.questions):
        correct, student_ans, correct_example = st.session_state.results[i]
        status = "Correct" if correct else "Incorrect"
        report += f"Q{i+1}: {fraction_to_str(low)} and {fraction_to_str(high)}\n"
        report += f"   Your answer: {student_ans}\n"
        if not correct:
            report += f"   Correct example: {fraction_to_str(correct_example)}\n"
        report += f"   Result: {status}\n\n"

    st.download_button(
        label="📥 Download Report (TXT)",
        data=report,
        file_name=f"{full_name.replace(' ', '_')}_fraction_quiz.txt",
        mime="text/plain"
    )

# ---------- Footer ----------
st.markdown("---")
st.caption("Enter a fraction like `1/2`, a decimal like `0.75`, or an integer like `5`. Fractions must be strictly between the two given numbers.")
