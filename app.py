import streamlit as st

st.set_page_config(page_title="Kangaroo Quest", page_icon="🦘")

st.title("🦘 Kangaroo Quest")
st.markdown("Welcome to Math Island! Solve puzzles to escape!")

questions = [
    {"question": "What comes next in 1, 1, 2, 3, 5, 8, ?", "options": ["10", "11", "13", "14"], "answer": "13"},
    {"question": "A square has area 36 cm². What's a side length?", "options": ["6", "18", "3", "12"], "answer": "6"},
    {"question": "What is 7 × 8 - 6 × 5?", "options": ["26", "31", "32", "33"], "answer": "31"},
]

score = 0

for i, q in enumerate(questions):
    st.subheader(f"Challenge {i+1}")
    user_answer = st.radio(q["question"], q["options"], key=i)
    if st.button(f"Submit Challenge {i+1}", key=i+100):
        if user_answer == q["answer"]:
            st.success("🎉 Correct!")
            score += 1
        else:
            st.error("❌ Try again!")

st.markdown("---")
st.write(f"Final Score: {score} / {len(questions)}")