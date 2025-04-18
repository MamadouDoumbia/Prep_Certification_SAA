import streamlit as st

# Fonction pour afficher le score à la fin du quiz
def show_score(user_answers_store, selected_session):
    correct_count = 0
    for idx, question_data in enumerate(selected_session):
        correct_answers = question_data['correct_answers']
        # Vérification de la réponse de l'utilisateur
        if sorted(user_answers_store.get(idx, [])) == sorted(correct_answers):
            correct_count += 1

    total_questions = len(selected_session)
    percentage = (correct_count / total_questions) * 100

    st.write(f"**Votre score final : {correct_count} sur {total_questions}**")
    st.write(f"**Pourcentage : {percentage:.2f}%**")

    if percentage >= 80:
        st.success("Félicitations, vous avez très bien réussi !")
    elif percentage >= 50:
        st.warning("Bon travail, mais vous pouvez encore améliorer votre score.")
    else:
        st.error("Essayez encore une fois, vous pouvez faire mieux !")

# Fonction pour mettre à jour la barre de progression
def update_progress(answered_questions, total_questions, progress_bar, progress_label):
    progress = (answered_questions / total_questions)  # Calcul de la progression en pourcentage
    progress = max(0, min(progress, 1))  # Assurer que la valeur est entre 0 et 1
    progress_bar.progress(progress)  # Mettre à jour la barre de progression
    progress_label.write(f"**Progression : {progress * 100:.2f}%**")  # Afficher la progression sous forme de pourcentage
