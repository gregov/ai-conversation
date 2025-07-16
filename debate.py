import os
import google.generativeai as genai
from dotenv import load_dotenv

# Charger la clé API Gemini depuis le fichier .env ou la variable d'environnement
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Veuillez définir la clé API Gemini dans GEMINI_API_KEY.")
genai.configure(api_key=API_KEY)

# Prompts de rôle
CONSERVATEUR = "Tu es un modèle d'IA qui défend un point de vue conservateur, avec courtoisie et argumentation."
PROGRESSISTE = "Tu es un modèle d'IA qui défend un point de vue progressiste, avec courtoisie et argumentation."

# Fonction pour générer une réponse

def get_response(model, role_prompt, sujet, previous_message=None):
    prompt = f"{role_prompt}\nSujet: {sujet}"
    if previous_message:
        prompt += f"\nTon interlocuteur a dit : {previous_message}\nRéponds-lui en challengeant ses arguments, toujours poliment."
    response = model.generate_content(prompt)
    return response.text.strip()


def main():
    # Decommenter pour lister les modèles disponibles
    # print([m.name for m in genai.list_models()])

    print("Bienvenue dans Gemini Debate Bot !")
    sujet = input("Sujet du débat : ")
    model_conservateur = genai.GenerativeModel("models/gemini-2.0-flash")
    model_progressiste = genai.GenerativeModel("models/gemini-2.0-flash")

    print("\nDébat :\n")
    message_c = get_response(model_conservateur, CONSERVATEUR, sujet)
    print(f"Conservateur : {message_c}\n")
    message_p = get_response(model_progressiste, PROGRESSISTE, sujet, previous_message=message_c)
    print(f"Progressiste : {message_p}\n")

    # Boucle de débat (3 tours)
    for i in range(2):
        message_c = get_response(model_conservateur, CONSERVATEUR, sujet, previous_message=message_p)
        print(f"Conservateur : {message_c}\n")
        message_p = get_response(model_progressiste, PROGRESSISTE, sujet, previous_message=message_c)
        print(f"Progressiste : {message_p}\n")

    print("Débat terminé. Merci d'avoir utilisé Gemini Debate Bot !")

if __name__ == "__main__":
    main()
