import streamlit as st
import json

# Charger les questions depuis le fichier JSON
def load_questions():
    with open('questions_answers.json', 'r') as file:
        return json.load(file)

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

# Afficher les questions une par une
for idx, question_data in enumerate(questions):
    st.write(f"### Question {idx + 1}")
    display_question(question_data, idx)
    st.markdown("---")  # Séparateur entre les questions
