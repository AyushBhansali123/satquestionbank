# game_engine.py
import streamlit as st

class SATImageGame:
    def __init__(self, images, answers):
        self.images = images
        self.answers = answers
        self.total_questions = len(images)

        if 'q_index' not in st.session_state:
            st.session_state.q_index = 0
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'finished' not in st.session_state:
            st.session_state.finished = False
        if 'show_result' not in st.session_state:
            st.session_state.show_result = False
        if 'last_correct' not in st.session_state:
            st.session_state.last_correct = None

    def current_image(self):
        return self.images[st.session_state.q_index]

    def current_answer(self):
        if st.session_state.q_index < len(self.answers):
            return self.answers[st.session_state.q_index]
        return None

    def submit_answer(self, user_answer):
        correct_answer = self.current_answer()

        if correct_answer:
            is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
            st.session_state.last_correct = is_correct
            if is_correct:
                st.session_state.score += 1
        else:
            st.session_state.last_correct = None

        st.session_state.show_result = True

    def next_question(self):
        st.session_state.show_result = False

        if st.session_state.q_index < self.total_questions - 1:
            st.session_state.q_index += 1
        else:
            st.session_state.finished = True

    def restart_game(self):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.finished = False
        st.session_state.show_result = False
