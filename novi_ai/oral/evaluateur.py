import json
import os
from groq import Groq
from novi_ai.models.ai_client import appeler_ia
from dotenv import load_dotenv

load_dotenv()

client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcrire_audio(chemin_audio: str) -> str:
    print("Transcription Groq Whisper...")
    with open(chemin_audio, "rb") as f:
        transcription = client_groq.audio.transcriptions.create(
            file=(os.path.basename(chemin_audio), f.read()),
            model="whisper-large-v3-turbo",
            language="fr",
            response_format="text"
        )
    return transcription

def evaluer_reponse(question: str, reponse_transcrite: str, criteres: list) -> dict:
    print("Évaluation IA...")

    eval_brut = appeler_ia([
        {
            "role": "system",
            "content": "Tu es un évaluateur pédagogique pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Évalue cette réponse orale.

Question : {question}
Réponse : {reponse_transcrite}
Critères : {', '.join(criteres)}

Réponds UNIQUEMENT en JSON :
{{
  "score": 0-100,
  "mention": "Insuffisant/Passable/Bien/Très Bien/Excellent",
  "points_forts": ["point 1", "point 2"],
  "points_ameliorer": ["point 1", "point 2"],
  "feedback_detaille": "feedback constructif de 3-4 phrases",
  "reponse_ideale": "ce qu'aurait dû contenir la réponse idéale"
}}"""
        }
    ], max_tokens=800, temperature=0.3)

    return json.loads(eval_brut[eval_brut.find("{"):eval_brut.rfind("}")+1])