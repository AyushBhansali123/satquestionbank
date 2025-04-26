# app.py
import streamlit as st
from pdf_parser import extract_question_images_from_pdf, extract_correct_answers_from_pdf
from game_engine import SATImageGame

st.set_page_config(page_title="SAT Image Game v2", layout="wide")

st.title("🎯 SAT Practice — Duolingo Style (Images)")

uploaded_questions_file = st.file_uploader("📄 Upload your SAT Questions PDF (no answers)", type=["pdf"])
uploaded_answers_file = st.file_uploader("📄 Upload your SAT Correct Answers PDF", type=["pdf"])

if uploaded_questions_file and uploaded_answers_file:
    with st.spinner('🔄 Loading your SAT Practice...'):
        with open("questions_temp.pdf", "wb") as f:
            f.write(uploaded_questions_file.read())
        with open("answers_temp.pdf", "wb") as f:
            f.write(uploaded_answers_file.read())

        images = extract_question_images_from_pdf("questions_temp.pdf")
        answers = extract_correct_answers_from_pdf("answers_temp.pdf")

    if not images or not answers:
        st.error("❗ Problem extracting questions or answers.")
    else:
        game = SATImageGame(images, answers)

        if not st.session_state.finished:

            st.progress((st.session_state.q_index + 1) / game.total_questions)

            # Now we check what to display
            if st.session_state.show_result:
                # Showing Result Screen
                if st.session_state.last_correct:
                    st.success("✅ Correct! 🎉")
                else:
                    correct_ans = game.current_answer()
                    st.error(f"❌ Incorrect. Correct Answer: {correct_ans}")

                if st.button("➡️ Next Question"):
                    game.next_question()

            else:
                # Showing Question Screen
                st.subheader(f"Question {st.session_state.q_index + 1} of {game.total_questions}")

                question_image = game.current_image()
                st.image(question_image, use_column_width=True)

                # User input and instant submit
                user_answer = st.text_input("✏️ Your Answer (A, B, C, D, etc.)", key=f"answer_{st.session_state.q_index}")

                if user_answer:  # As soon as there is input, we can show "Submit" button
                    if st.button("✅ Check Answer"):
                        game.submit_answer(user_answer)

        else:
            st.balloons()
            st.success(f"🏆 Finished! Your Final Score: {st.session_state.score}")

            if st.button("🔄 Play Again"):
                SATImageGame([], []).restart_game()

else:
    st.info("👆 Upload both the Questions PDF and the Answers PDF to start.")
