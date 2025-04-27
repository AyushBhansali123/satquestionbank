# game_engine.py
import streamlit as st
import time

class SATImageGame:
    def __init__(self, images, answers, explanations):
        self.images = images
        self.answers = answers
        self.explanations = explanations
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
        if 'start_time' not in st.session_state:
            st.session_state.start_time = time.time()
        if 'auto_submitted' not in st.session_state:
            st.session_state.auto_submitted = False

    def current_image(self):
        return self.images[st.session_state.q_index]

    def current_answer(self):
        if st.session_state.q_index < len(self.answers):
            return self.answers[st.session_state.q_index]
        return None

    def current_explanation(self):
        if st.session_state.q_index < len(self.explanations):
            return self.explanations[st.session_state.q_index]
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
        st.session_state.auto_submitted = False
        st.session_state.start_time = time.time()

        if st.session_state.q_index < self.total_questions - 1:
            st.session_state.q_index += 1
        else:
            st.session_state.finished = True

    def restart_game(self):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.finished = False
        st.session_state.show_result = False
        st.session_state.last_correct = None
        st.session_state.start_time = time.time()
        st.session_state.auto_submitted = False

    def check_timer_and_auto_submit(self, user_answer):
        elapsed = time.time() - st.session_state.start_time
        if elapsed > 90 and not st.session_state.show_result and not st.session_state.auto_submitted:
            self.submit_answer(user_answer if user_answer else "")
            st.session_state.auto_submitted = True

    def auto_continue_after_feedback(self):
        if st.session_state.show_result:
            elapsed = time.time() - st.session_state.start_time
            if elapsed > 91:  # 90 for question, 1 for feedback
                self.next_question()
