import re
import json

# Nom du fichier texte à lire
input_filename = 'questions.txt'
output_filename = 'questions_answers.json'

# Fonction pour extraire les données du fichier texte
def extract_questions_and_answers(file_content):
    questions_data = []

    # Trouver les questions et leurs réponses avec une regex
    questions = re.findall(r'Question #(\d+.*?)\n(.*?)(?=Question #|$)', file_content, re.DOTALL)
    questions = re.findall(r'(Question #\d+.*?)\n\n(.*?)(?=Community vote distribution|$)', file_content, re.DOTALL)


    for question_id, (question_text, answers_text) in enumerate(questions, 1):  # On commence à 1 pour le numéro de la question
        # Nettoyer le texte de la question
        question_text = question_text.strip()

        # Extraire les réponses sous la forme (A. réponse, B. réponse, C. réponse, D. réponse)
        answers = re.findall(r'\s{4}([A-D])\.(.*?)\n', answers_text)
        
        # Liste des réponses avec leur statut de correction
        answers_list = [{"text": answer.strip(), "is_correct": False} for _, answer in answers]

        # Identifier la bonne réponse en cherchant "Most Voted" ou "Correct Answer:"
        correct_answers = []
        for idx, (_, answer) in enumerate(answers):
            # Vérifier si la réponse contient "Most Voted" ou "Correct Answer:"
            if "Most Voted" in answer or "Correct Answer" in answer:
                answers_list[idx]["is_correct"] = True
                correct_answers.append(answer.strip())

        # Ajouter l'ID de la question dans les données
        questions_data.append({
            "id": question_id,
            "question": question_text,
            "answers": answers_list,
            "correct_answers": correct_answers
        })
    
    return questions_data

# Lire le fichier texte
with open(input_filename, 'r') as file:
    file_content = file.read()

# Extraire les données des questions et réponses
questions_data = extract_questions_and_answers(file_content)

# Sauvegarder dans un fichier JSON
with open(output_filename, 'w') as json_file:
    json.dump(questions_data, json_file, indent=4)

print(f"Les questions et réponses ont été extraites et sauvegardées dans '{output_filename}'")
