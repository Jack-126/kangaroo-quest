import streamlit as st

questions = [
    {"question": "What is the value of $\\frac{20 \\times 24}{(2 \\times 0) + (2 \\times 4)}$?", 
     "options": ["12", "30", "48", "60", "120"], 
     "answer": "60", 
     "hint": "Carefully calculate both numerator and denominator. Remember, 2×0 is 0."},
    
    {"question": "The angles in a triangle are in the ratio 1:3:5. What is the biggest of those angles?", 
     "options": ["80°", "90°", "100°", "110°", "120°"], 
     "answer": "100°", 
     "hint": "The sum of angles in a triangle is 180°. Use the ratio to split 180°."},
    
    {"question": "Lizzy has 7 coins of a kind. She buys three fruits at the market. Each fruit has a different price. How much is the most expensive fruit?", 
     "options": ["2", "3", "4", "5", "6"], 
     "answer": "4", 
     "hint": "Try adding different combinations of 3 different numbers that total 7."},
    
    {"question": "A square has a perimeter of 32 cm. The square is cut into 4 equal strips. What is the perimeter of once such strip?", 
     "options": ["16 cm", "20 cm", "22 cm", "24 cm", "26 cm"], 
     "answer": "20 cm", 
     "hint": "First find the side of the square, then draw and cut it into strips to understand the new shape."},
    
    {"question": "Ria has three cards with the numbers 1, 5 and 11. She wants to place the cards next to each other to form a 4-digit number. How many different 4-digit numbers can she form?", 
     "options": ["3", "4", "6", "8", "9"], 
     "answer": "4", 
     "hint": "The digit '11' is actually not valid; split it into 1 and 1. How many ways can you arrange 1, 1, 5, and 1 more digit?"},
    
    {"question": "How many three-digit numbers are there that contain at least one of the digits 1, 2 or 3?", 
     "options": ["27", "147", "441", "557", "606"], 
     "answer": "606", 
     "hint": "There are 900 three-digit numbers in total (from 100 to 999). Instead of counting how many do have 1, 2, or 3, it's easier to count how many do not have any of them and subtract."},
    
    {"question": "The number 2024 is made up of the four digits 2, 0, 2 and 4. How many different four-digit numbers bigger than 2024 can be formed with exactly those digits?", 
     "options": ["4", "5", "6", "7", "8"], 
     "answer": "8", 
     "hint": "List all possible 4-digit numbers using those digits, being careful not to repeat or start with 0. Then count only the ones bigger than 2024."},
    
    {"question": "Which of the following numbers is two less than a multiple of ten, two more than a square number and two times a prime number?", 
     "options": ["78", "58", "38", "18", "6"], 
     "answer": "38", 
     "hint": "List multiple of ten = (10, 20, 30, 40, 50, 60, 70, 80, …), List square numbers = (1, 4, 9, 16, 25, 36, 49, 64, 81, …), List prime numbers = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, …)."},
    
    {"question": "Uli can buy exactly 12 packages of jelly babies or exactly 20 chocolate bars with her pocket money. Uli buys 9 packages of jelly babies. How many chocolate bars can she buy with the remaining money?", 
     "options": ["3", "4", "5", "6", "8"], 
     "answer": "5", 
     "hint": " Let x be the total money. Set up ratios to find remaining amount and divide by chocolate bar price."},
    
    {"question": "How many integers k have the property that k+6 is a multiple of k-6?", 
     "options": ["0", "4", "6", "8", "12"], 
     "answer": "12", 
     "hint": "Let the expression $\\frac{k+6}{k-6}$ be an integer. Try small integer values of k and see when the division is exact."}
]

num_qs = len(questions)

st.set_page_config(page_title="Kangaroo Quest", page_icon="🦘")
st.title("🦘 Kangaroo Quest")
st.markdown(f"Solve all {num_qs} math puzzles to escape Math Island!")

# Initialize ALL session state variables in one place
if 'init' not in st.session_state:
    st.session_state.update({
        'score': 0,
        'unlocked': [True] + [False]*(num_qs-1),  # First question unlocked
        'correct_answers': [False]*num_qs,
        'feedback': [None]*num_qs,
        'current_question': 0,
        'attempts': [0]*num_qs,
        'show_hint': [False]*num_qs,
        'init': True  # Marks initialization complete
    })

def show_feedback(question_idx, is_correct):
    if is_correct:
        if not st.session_state.correct_answers[question_idx]:
            st.session_state.correct_answers[question_idx] = True
            st.session_state.score += 1
        st.session_state.feedback[question_idx] = (
            f"✅ Correct! The answer is {questions[question_idx]['answer']}!",True)
        # Unlock next question if not last
        if question_idx < num_qs-1 and not st.session_state.unlocked[question_idx+1]:
            st.session_state.unlocked[question_idx+1] = True
    else:
        st.session_state.attempts[question_idx] += 1
        # Show hint after first wrong attempt
        st.session_state.show_hint[question_idx] = True
        
        if st.session_state.attempts[question_idx] >= 3:
            st.session_state.feedback[question_idx] = (
                f"❌ Skipped after 3 attempts. Correct answer: {questions[question_idx]['answer']}",
                False
            )
            # Auto-advance if not last question
            if question_idx < num_qs-1:
                st.session_state.current_question += 1
                st.rerun()
        else:
            st.session_state.feedback[question_idx] = (
                "❌ Incorrect. Try again!",
                False
            )

# Current question
i = st.session_state.current_question
q = questions[i]

# Display
st.subheader(f"Question {i+1} of {len(questions)}")
st.write(f"**{q['question']}**")

user_answer = st.radio(
    "Select your answer:",
    q["options"],
    key=f"q{i}"
)

if st.button("Submit"):
    show_feedback(i, user_answer == q["answer"])

# Feedback area
if st.session_state.feedback[i]:
    msg, is_correct = st.session_state.feedback[i]
    if is_correct:
        st.success(msg)
        if st.button("Next Question"):
            if st.session_state.current_question < num_qs-1:
                st.session_state.current_question += 1
                st.rerun()
    else:
        st.error(msg)
    
    # Show hint if applicable
    if not is_correct and st.session_state.show_hint[i]:
        st.info(f"💡 Hint: {q['hint']}")
    
    # Show attempts remaining
    if not is_correct and st.session_state.attempts[i] < 3:
        st.warning(f"Attempts left: {3 - st.session_state.attempts[i]}")

# YOUR PROGRESS TRACKER (fixed)
st.markdown("---")
st.subheader("Question Progress")
cols = st.columns(5)
for idx in range(num_qs):
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
st.subheader(f"🏁 Score: {st.session_state.score}/{num_qs}")
# Show summary if final question answered or skipped
if all(st.session_state.feedback):
    st.markdown("---")
    if st.session_state.score == num_qs:
        st.balloons()
        st.success("🎉 You've escaped Math Island!")
    else:
        st.info("🔒 You didn’t solve all the puzzles correctly. Try again to escape Math Island!")

    st.markdown("---")
    st.subheader("📘 Summary")
    for idx, q in enumerate(questions):
        st.markdown(f"**Q{idx+1}**: {q['question']}")
        st.markdown("**Options:**")
        for opt in q['options']:
            st.markdown(f"- {opt}")
        st.markdown(f"**Answer**: {q['answer']}")
        st.markdown("---")
        
if st.button("🔁 Restart Game"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()