import streamlit as st
import json
import random

# Charger les questions depuis le fichier JSON avec gestion des erreurs
def load_questions():
    try:
        with open('questions_answers.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Le fichier 'questions_answers.json' est introuvable. Veuillez vérifier le chemin.")
        return []
    except json.JSONDecodeError:
        st.error("Erreur lors de la lecture du fichier JSON. Assurez-vous qu'il est correctement formaté.")
        return []

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
        random.shuffle(session)  # Mélanger les questions dans chaque session
    return sessions

# Fonction pour afficher une question et collecter les réponses
def display_question(question_data, idx, user_answers_store):
    st.write(f"**Question**: {question_data['question']}")
    answers = question_data['answers']
    correct_answers = question_data['correct_answers']

    if len(correct_answers) > 1:
        selected_answers = []
        # Lors de l'affichage des cases à cocher, les cases ne sont pas cochées par défaut
        for ans in answers:
            if st.checkbox(ans['text'], key=f"answer_{idx}_{ans['text']}", value=False):  # Pas de valeur par défaut (False)
                selected_answers.append(ans['text'])
        user_answers_store[idx] = selected_answers
    else:
        # Pour une seule réponse, utiliser un bouton radio sans spécifier d'index par défaut
        selected_answer = st.radio("Sélectionnez votre réponse:", [ans['text'] for ans in answers], key=f"question_{idx}", index=None)  # Pas de valeur par défaut
        user_answers_store[idx] = [selected_answer] if selected_answer else []

# Fonction pour afficher le score à la fin du quiz
def show_score(user_answers_store, selected_session):
    correct_count = 0
    for idx, question_data in enumerate(selected_session):
        correct_answers = question_data['correct_answers']
        if sorted(user_answers_store[idx]) == sorted(correct_answers):
            correct_count += 1

    total_questions = len(selected_session)
    percentage = (correct_count / total_questions) * 100

    st.write(f"**Votre score final : {correct_count} sur {total_questions}**")
    st.write(f"**Pourcentage : {percentage:.2f}%**")

# Titre de l'application
st.title("Amazon S3 Question Quiz")

# Charger les questions (chargées une seule fois)
if 'questions' not in st.session_state:
    questions = load_questions()
    if questions:  # Si des questions ont été chargées
        st.session_state.questions = questions

# Diviser les questions en sessions (une seule fois)
if 'sessions' not in st.session_state and 'questions' in st.session_state:
    sessions = split_into_sessions(st.session_state.questions)
    st.session_state.sessions = sessions

# Mélanger les questions dans chaque session (une seule fois)
if 'shuffled_sessions' not in st.session_state and 'sessions' in st.session_state:
    shuffled_sessions = shuffle_sessions(st.session_state.sessions)
    st.session_state.shuffled_sessions = shuffled_sessions

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
selected_session = st.session_state.shuffled_sessions[session_map[session_choice]]

# Dictionnaire pour stocker les réponses de l'utilisateur
user_answers_store = {}

# Initialiser la barre de progression et le pourcentage
total_questions = len(selected_session)
answered_questions = 0

# Afficher la barre de progression et le pourcentage en haut de la page (avant les questions)
progress = (answered_questions / total_questions)
progress = max(0, min(progress, 1))  # Assurer que la valeur est entre 0 et 1
progress_bar = st.progress(progress)  # Afficher la barre de progression
progress_label = st.empty()  # Création d'un espace vide pour le pourcentage

# Calculer la progression initiale
progress_label.write(f"**Progression : {progress * 100:.2f}%**")  # Afficher le pourcentage juste à côté

st.markdown("---")  # Ligne séparatrice pour bien séparer la barre de progression des questions

# Afficher les questions de la session sélectionnée
for idx, question_data in enumerate(selected_session):
    st.write(f"### Question {idx + 1}")
    display_question(question_data, idx, user_answers_store)

    # Bouton "Répondre" sous chaque question
    if st.button("Répondre", key=f"submit_{idx}"):
        # Mettre à jour les réponses de l'utilisateur
        st.write(f"Réponse donnée pour la question {idx + 1}: {user_answers_store[idx]}")

        # Mettre à jour la progression après chaque réponse (sans réafficher le pourcentage sous la question)
        answered_questions = len(user_answers_store)
        progress = (answered_questions / total_questions)
        progress = max(0, min(progress, 1))  # Assurer que la valeur est entre 0 et 1
        progress_bar.progress(progress)  # Mettre à jour la barre de progression

        # Mettre à jour le pourcentage
        progress_label.write(f"**Progression : {progress * 100:.2f}%**")  # Réafficher le pourcentage

    st.markdown("---")  # Ligne séparatrice après chaque question

# Afficher le bouton "Voir le score" une seule fois après toutes les questions
if len(user_answers_store) == total_questions:
    if st.button("Voir le score"):
        show_score(user_answers_store, selected_session)
elif len(user_answers_store) < total_questions:
    st.warning("Veuillez répondre à toutes les questions avant de voir votre score.")
