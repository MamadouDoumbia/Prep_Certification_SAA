import streamlit as st
import json
import random

# Charger les questions depuis le fichier JSON
def load_questions():
    with open('questions_answers.json', 'r') as file:
        return json.load(file)

# Diviser les questions en 4 sessions
def split_into_sessions(questions):
    session_size = 65
    sessions = []

    for i in range(3):
        sessions.append(questions[i * session_size:(i + 1) * session_size])

    sessions.append(questions[3 * session_size:])
    return sessions

# Mélanger les questions dans chaque session
def shuffle_sessions(sessions):
    for session in sessions:
        random.shuffle(session)
    return sessions

# Fonction pour afficher une question et collecter les réponses
def display_question(question_data, idx, user_answers_store):
    st.write(f"**Question**: {question_data['question']}")
    answers = question_data['answers']
    correct_answers = question_data['correct_answers']

    if len(correct_answers) > 1:
        # Cases à cocher pour plusieurs réponses correctes
        selected_answers = []
        for ans in answers:
            if st.checkbox(ans['text'], key=f"answer_{idx}_{ans['text']}"):
                selected_answers.append(ans['text'])
        user_answers_store[idx] = selected_answers
    else:
        # Boutons radio pour une seule réponse correcte
        selected_answer = st.radio("Select your answer:", [ans['text'] for ans in answers], key=f"question_{idx}")
        user_answers_store[idx] = [selected_answer]

    # Bouton pour soumettre la réponse et vérifier
    if st.button("Répondre", key=f"submit_{idx}"):
        if sorted(user_answers_store[idx]) == sorted(correct_answers):
            st.success("Correct!")
        else:
            st.error(f"Incorrect. The correct answers are: {', '.join(correct_answers)}")

# Fonction pour afficher le score à la fin du quiz
def show_score(user_answers_store, selected_session):
    correct_count = 0
    for idx, question_data in enumerate(selected_session):
        correct_answers = question_data['correct_answers']
        if sorted(user_answers_store[idx]) == sorted(correct_answers):
            correct_count += 1
    st.write(f"**Your final score: {correct_count} out of {len(selected_session)}**")

# Titre de l'application
st.title("Amazon S3 Question Quiz")

# Charger les questions
questions = load_questions()

# Diviser les questions en sessions
sessions = split_into_sessions(questions)

# Mélanger les questions de chaque session
sessions = shuffle_sessions(sessions)

# Créer une sidebar pour la sélection de session
session_choice = st.sidebar.radio("Choisir une session", ["Session 1", "Session 2", "Session 3", "Session 4"])

# Dictionnaire pour lier les sessions aux indices
session_map = {
    "Session 1": 0,
    "Session 2": 1,
    "Session 3": 2,
    "Session 4": 3
}

# Obtenir les questions de la session choisie
selected_session = sessions[session_map[session_choice]]

# Dictionnaire pour stocker les réponses de l'utilisateur
user_answers_store = {}

# Afficher les questions de la session sélectionnée
for idx, question_data in enumerate(selected_session):
    st.write(f"### Question {idx + 1}")
    display_question(question_data, idx, user_answers_store)
    st.markdown("---")

# Afficher le score à la fin du quiz
if st.button("Voir le score"):
    show_score(user_answers_store, selected_session)
