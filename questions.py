import json
import random

# Charger les questions depuis le fichier JSON avec gestion des erreurs
def load_questions(file_path='questions_answers.json'):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Le fichier 'questions_answers.json' est introuvable.")
        return []
    except json.JSONDecodeError:
        print("Erreur lors de la lecture du fichier JSON.")
        return []

# Diviser les questions en sessions (par défaut 4 sessions)
def split_into_sessions(questions, num_sessions=4):
    session_size = len(questions) // num_sessions
    sessions = [questions[i * session_size:(i + 1) * session_size] for i in range(num_sessions-1)]
    sessions.append(questions[(num_sessions-1) * session_size:])  # Dernière session avec le reste
    return sessions

# Mélanger les questions dans chaque session
def shuffle_sessions(sessions):
    for session in sessions:
        random.shuffle(session)  # Mélanger les questions dans chaque session
    return sessions
