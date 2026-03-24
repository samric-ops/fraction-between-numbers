import streamlit as st
from fractions import Fraction

st.set_page_config(page_title="Fraction Between Two Numbers", page_icon="🔢")
st.title("🔢 Find a Fraction Between Two Numbers")
st.markdown("Enter two rational numbers and your name to get a fraction that lies strictly between them.")

# ------------------ Name Input ------------------
st.subheader("Student Information")
col1, col2, col3 = st.columns(3)
with col1:
    surname = st.text_input("Surname", placeholder="e.g., Dela Cruz")
with col2:
    first_name = st.text_input("First Name", placeholder="e.g., Juan")
with col3:
    middle_initial = st.text_input("Middle Initial (optional)", max_chars=1, placeholder="M")

full_name = f"{surname} {first_name} {middle_initial}".strip() if middle_initial else f"{surname} {first_name}".strip()

# ------------------ Number Input ------------------
st.subheader("Enter Two Numbers")
num1_str = st.text_input("First number", placeholder="e.g., 1/3, 0.75, 2")
num2_str = st.text_input("Second number", placeholder="e.g., 2/3, 1.25, 5")

# ------------------ Computation ------------------
if st.button("Find Fraction Between"):
    if not surname or not first_name:
        st.error("Please enter at least your surname and first name.")
    elif not num1_str or not num2_str:
        st.error("Please enter both numbers.")
    else:
        try:
            # Convert inputs to Fraction (handles fractions, decimals, integers)
            a = Fraction(num1_str)
            b = Fraction(num2_str)

            if a == b:
                st.error("The two numbers are equal. There is no rational number strictly between them.")
            else:
                # Compute the average
                result_frac = (a + b) / 2
                result_decimal = float(result_frac)

                st.success("✅ A fraction between the two numbers is found!")
                st.write(f"**Between** `{a}` and `{b}`")
                st.write(f"**Fraction:** `{result_frac}`")
                st.write(f"**Decimal approximation:** `{result_decimal:.6f}`")

                # Prepare download content
                download_content = f"""
STUDENT OUTPUT
================================

Student Name: {full_name}

Given Numbers:
  First number  : {a}
  Second number : {b}

A rational number between them:
  As fraction   : {result_frac}
  As decimal    : {result_decimal:.6f}

Generated on: {st.session_state.get('timestamp', 'N/A')}
                """
                # Add timestamp to session state if not present
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                download_content = download_content.replace('N/A', timestamp)

                st.download_button(
                    label="📥 Download Output",
                    data=download_content,
                    file_name=f"{full_name.replace(' ', '_')}_output.txt",
                    mime="text/plain"
                )
                # Store timestamp for next downloads
                st.session_state['timestamp'] = timestamp

        except Exception as e:
            st.error(f"Invalid number format. Please use numbers like 2, 0.75, 1/3, etc. Error: {e}")

# Optional: Show examples
with st.expander("ℹ️ How to use"):
    st.markdown("""
    - **Numbers** can be entered as:
        - Decimals: `0.5`, `2.75`
        - Fractions: `3/4`, `1/2`
        - Integers: `5`, `-3`
    - The app will compute the **average** and simplify it to a fraction.
    - If the two numbers are equal, no fraction exists between them – you'll see an error.
    - After clicking the button, a download button appears – click it to save your output as a text file.
    """)
