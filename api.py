import streamlit as st
import json

# Charger les questions depuis le fichier JSON
def load_questions():
    with open('questions_answers.json', 'r') as file:
        return json.load(file)

# Diviser les questions en 4 sessions
def split_into_sessions(questions):
    session_size = 65  # Taille de chaque session sauf la dernière
    sessions = []

    # Diviser en 3 sessions de 65
    for i in range(3):
        sessions.append(questions[i * session_size:(i + 1) * session_size])

    # Dernière session avec 54 questions
    sessions.append(questions[3 * session_size:])

    return sessions

# Fonction pour afficher une question avec des boutons radio ou des cases à cocher
def display_question(question_data, idx):
    st.write(f"**Question**: {question_data['question']}")

    answers = question_data['answers']
    correct_answers = question_data['correct_answers']

    # Si plusieurs bonnes réponses, afficher des cases à cocher
    if len(correct_answers) > 1:
        user_answers = []
        for ans in answers:
            if st.checkbox(ans['text'], key=f"answer_{ans['text']}"):
                user_answers.append(ans['text'])
    else:
        # Si une seule bonne réponse, afficher des boutons radio
        user_answers = st.radio("Select your answer:", [ans['text'] for ans in answers], key=f"question_{idx}")
        user_answers = [user_answers]  # Pour uniformiser la structure (liste même pour une seule réponse)

    # Bouton pour soumettre la réponse et vérifier
    if st.button("Répondre", key=f"submit_{idx}"):
        # Comparer les réponses de l'utilisateur avec les bonnes réponses
        if sorted(user_answers) == sorted(correct_answers):
            st.success("Correct!")
        else:
            st.error(f"Incorrect. The correct answers are: {', '.join(correct_answers)}")

# Titre de l'application
st.title("Amazon S3 Question Quiz")

# Charger les questions
questions = load_questions()

# Diviser les questions en sessions
sessions = split_into_sessions(questions)

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

# Afficher les questions de la session sélectionnée
for idx, question_data in enumerate(selected_session):
    st.write(f"### Question {idx + 1}")
    display_question(question_data, idx)
    st.markdown("---")  # Séparateur entre les questions
