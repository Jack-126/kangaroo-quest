import streamlit as st

st.set_page_config(page_title="Kangaroo Quest", page_icon="🦘")
st.title("🦘 Kangaroo Quest")
st.markdown("Solve all 15 math puzzles to escape Math Island!")

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "unlocked" not in st.session_state:
    st.session_state.unlocked = [False] * 15
    st.session_state.unlocked[0] = True
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = [False] * 15
if "feedback" not in st.session_state:
    st.session_state.feedback = [None] * 15
if "current_question" not in st.session_state:
    st.session_state.current_question = 0

questions = [
    {"question": "What comes next in 1, 1, 2, 3, 5, 8, ?", "options": ["10", "11", "13", "14"], "answer": "13", "hint": "Add the two previous numbers."},
    {"question": "A triangle has angles of 35° and 65°. What’s the third angle?", "options": ["80°", "90°", "100°", "85°"], "answer": "80°", "hint": "Triangle angles always add up to 180°."},
    {"question": "What is 7 × 8 − 6 × 5?", "options": ["26", "31", "32", "33"], "answer": "26", "hint": "Use brackets: (7×8) − (6×5)."},
    {"question": "A square has an area of 36 cm². What is the side length?", "options": ["3", "6", "12", "18"], "answer": "6", "hint": "Think: side × side = 36."},
    {"question": "Tom has 3 red, 2 blue, and 1 green balloon. How many ways to give 2 to a friend?", "options": ["6", "10", "12", "15"], "answer": "15", "hint": "Use combinations (6 choose 2)."},
    {"question": "2, 4, 8, 16, ?", "options": ["18", "20", "24", "32"], "answer": "32", "hint": "Each number doubles."},
    {"question": "Emma has RM1.80 in 10c and 20c coins (12 coins). How many 20c coins?", "options": ["3", "4", "5", "6"], "answer": "3", "hint": "Try solving: 10x + 20y = 180, x+y = 12."},
    {"question": "Which letter looks the same in a mirror?", "options": ["A", "B", "H", "F"], "answer": "H", "hint": "Check symmetry by drawing it."},
    {"question": "How many ways to go 3 right and 2 up?", "options": ["6", "10", "12", "15"], "answer": "10", "hint": "Use combination: 5 choose 2."},
    {"question": "What’s the angle between clock hands at 3:00?", "options": ["60°", "90°", "120°", "150°"], "answer": "90°", "hint": "Each hour = 30°, and they're 3 hours apart."},
    {"question": "Find the 100th digit in 123123...", "options": ["1", "2", "3", "None"], "answer": "1", "hint": "Pattern repeats every 3 digits."},
    {"question": "How many ways for frog to jump 5 steps (1 or 2 steps)?", "options": ["5", "8", "10", "12"], "answer": "8", "hint": "Fibonacci pattern."},
    {"question": "Cut 3×4 rectangle into 1×1 squares — how many cuts?", "options": ["7", "8", "11", "12"], "answer": "11", "hint": "Cuts = rows-1 + cols-1."},
    {"question": "If apple + 2 bananas = 10 and banana = 2, what’s the apple worth?", "options": ["3", "4", "5", "6"], "answer": "6", "hint": "a + 2×2 = 10 → a = ?"},
    {"question": "Stick 1m → 0.5m shadow; giraffe shadow = 2m. How tall?", "options": ["3m", "4m", "2m", "5m"], "answer": "4m", "hint": "Use ratio: height/shadow = constant."},
]

def show_feedback(question_idx, is_correct):
    if is_correct:
        correct_answer = questions[question_idx]["answer"]
        st.session_state.feedback[question_idx] = (
            f"✅ Correct! The answer is {correct_answer}",
            True
        )
    else:
        hint = questions[question_idx]["hint"]
        st.session_state.feedback[question_idx] = (
            f"❌ Incorrect. Hint: {hint}",
            False
        )

# Display current question
i = st.session_state.current_question
q = questions[i]

st.subheader(f"Challenge {i+1}")
user_answer = st.radio(
    q["question"],
    q["options"],
    key=f"q{i}"
)

if st.button(f"Submit Question {i+1}", key=f"submit{i}"):
    if user_answer == q["answer"]:
        show_feedback(i, True)
        if not st.session_state.correct_answers[i]:
            st.session_state.score += 1
            st.session_state.correct_answers[i] = True
    else:
        show_feedback(i, False)

# Show feedback after submit
if st.session_state.feedback[i]:
    msg, is_correct = st.session_state.feedback[i]
    if is_correct:
        st.success(msg)
        if i < len(questions) - 1:
            if st.button("➡️ Next Question"):
                st.session_state.current_question += 1
                st.rerun()
        else:
            st.success("🎉 You've finished all questions!")
    else:
        st.error(msg)

# Show progress tracker
st.markdown("---")
st.subheader("Question Progress")
cols = st.columns(5)
for idx in range(len(questions)):
    with cols[idx % 5]:
        if st.session_state.correct_answers[idx]:
            st.success(f"{idx+1} ✅")
        elif idx == st.session_state.current_question:
            st.info(f"{idx+1} ➤")
        elif idx < st.session_state.current_question:
            st.warning(f"{idx+1} ✏️")
        else:
            st.error(f"{idx+1} 🔒")

# Score display
st.markdown("---")
st.subheader(f"🏁 Score: {st.session_state.score} / {len(questions)}")

if st.session_state.score == len(questions):
    st.balloons()
    st.success("🎉 You've escaped Math Island!")

    st.markdown("---")
    st.subheader("📘 Summary of All Questions & Answers")

    for idx, q in enumerate(questions):
        user_answer = st.session_state.get(f"q{idx}", "Not answered")
        correct = q["answer"]
        is_correct = (user_answer == correct)

        st.markdown(f"**Q{idx+1}: {q['question']}**")
        st.markdown("Options: " + ", ".join(q["options"]))
        st.markdown(f"- ✅ Correct Answer: **{correct}**")
        st.markdown("---")

elif st.session_state.score >= 10:
    st.info("🌟 Great progress! Keep going!")
