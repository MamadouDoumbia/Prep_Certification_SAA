import streamlit as st

# Fonction pour afficher une question et collecter les réponses
def display_question(question_data, idx, user_answers_store):
    st.write(f"**Question**: {question_data['question']}")
    answers = question_data['answers']
    correct_answers = question_data['correct_answers']

    if len(correct_answers) > 1:
        selected_answers = []
        for ans in answers:
            if st.checkbox(ans['text'], key=f"answer_{idx}_{ans['text']}", value=False):
                selected_answers.append(ans['text'])
        user_answers_store[idx] = selected_answers
    else:
        selected_answer = st.radio("Sélectionnez votre réponse:", [ans['text'] for ans in answers], key=f"question_{idx}", index=None)
        user_answers_store[idx] = [selected_answer] if selected_answer else []

# Fonction pour enregistrer la réponse de l'utilisateur
def store_answer(user_answers_store, idx, answer):
    user_answers_store[idx] = answer
