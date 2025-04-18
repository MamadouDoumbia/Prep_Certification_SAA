import streamlit as st
from questions import load_questions, split_into_sessions, shuffle_sessions
from quiz import display_question, store_answer
from score import show_score, update_progress
import time

def main():
    st.title("Amazon S3 Question Quiz")

    # Choix du mode
    quiz_mode = st.sidebar.radio("Choisir un mode", ["Réponse immédiate", "Mode réaliste (minuté)"])

    # Charger les questions et préparer les sessions
    if 'questions' not in st.session_state:
        st.session_state.questions = load_questions()

    if 'sessions' not in st.session_state and 'questions' in st.session_state:
        st.session_state.sessions = split_into_sessions(st.session_state.questions)

    if 'shuffled_sessions' not in st.session_state and 'sessions' in st.session_state:
        st.session_state.shuffled_sessions = shuffle_sessions(st.session_state.sessions)

    # Créer une sidebar pour la sélection de session
    session_choice = st.sidebar.radio("Choisir une session", ["Session 1", "Session 2", "Session 3", "Session 4"])
    session_map = {
        "Session 1": 0,
        "Session 2": 1,
        "Session 3": 2,
        "Session 4": 3
    }

    selected_session = st.session_state.shuffled_sessions[session_map[session_choice]]

    # Initialiser le store de réponses de l'utilisateur
    if 'user_answers_store' not in st.session_state:
        st.session_state.user_answers_store = {}

    # Si le mode est "Mode réaliste", initialiser le temps de début
    if quiz_mode == "Mode réaliste (minuté)" and 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    # Calculer le temps restant pour le mode minuté
    if quiz_mode == "Mode réaliste (minuté)":
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = max(0, 300 - elapsed_time)  # 5 minutes = 300 secondes
        minutes_left = int(remaining_time // 60)
        seconds_left = int(remaining_time % 60)

        # Afficher dynamiquement le temps restant
        time_display = st.empty()  # Créer un conteneur vide pour mettre à jour le temps restant
        time_display.write(f"Temps restant: {minutes_left}m {seconds_left}s")

        # Si le temps est écoulé, arrêter l'application
        if remaining_time <= 0:
            st.warning("Le temps est écoulé !")
            st.stop()

    # Initialiser la barre de progression dans session_state si non définie
    if 'progress' not in st.session_state:
        st.session_state.progress = 0  # Début de la progression à 0%

    total_questions = len(selected_session)

    # Calcul de la progression : nombre de réponses données / nombre total de questions
    answered_questions = len(st.session_state.user_answers_store)
    progress = answered_questions / total_questions  # Calcul de la progression en pourcentage

    # Mettre à jour la barre de progression dans session_state
    st.session_state.progress = progress  # Mise à jour de la progression dans session_state
    progress_bar = st.progress(st.session_state.progress)  # Mettre à jour la barre de progression
    progress_label = st.empty()

    # Afficher la progression en pourcentage
    progress_label.write(f"**Progression : {st.session_state.progress * 100:.2f}%**")

    st.markdown("---")

    # Affichage des questions
    for idx, question_data in enumerate(selected_session):
        st.write(f"### Question {idx + 1}")
        display_question(question_data, idx, st.session_state.user_answers_store)

        if st.button("Répondre", key=f"submit_{idx}"):
            store_answer(st.session_state.user_answers_store, idx, st.session_state.user_answers_store[idx])

            # Si mode "Réponse immédiate", afficher la réponse après chaque question
            if quiz_mode == "Réponse immédiate":
                correct_answers = question_data['correct_answers']
                user_answer = st.session_state.user_answers_store[idx]
                if sorted(user_answer) == sorted(correct_answers):
                    st.success("Bonne réponse !")
                else:
                    st.error(f"Mauvaise réponse. La bonne réponse est: {', '.join(correct_answers)}")

            # Mise à jour de la barre de progression après chaque réponse
            answered_questions = len(st.session_state.user_answers_store)  # Nombre de réponses données
            update_progress(answered_questions, total_questions, progress_bar, progress_label)  # Mise à jour de la progression

        st.markdown("---")

    # Si toutes les questions sont répondues, afficher le score
    if len(st.session_state.user_answers_store) == total_questions:
        if st.button("Voir le score"):
            show_score(st.session_state.user_answers_store, selected_session)

    elif len(st.session_state.user_answers_store) < total_questions:
        st.warning("Veuillez répondre à toutes les questions avant de voir votre score.")

if __name__ == "__main__":
    main()
