import json
import os
import time
from dotenv import load_dotenv
from novi_ai.models.ai_client import appeler_ia

load_dotenv()

def generer_avec_groq(messages, max_tokens=4000):
    return appeler_ia(messages, max_tokens=max_tokens, temperature=0.7)

def extraire_json(texte: str) -> dict:
    debut = texte.find("{")
    fin = texte.rfind("}") + 1
    if debut == -1 or fin == 0:
        raise ValueError("JSON non trouvé")
    return json.loads(texte[debut:fin])

def generer_plan(sujet: str, niveau: str) -> dict:
    print(f"Génération du plan : {sujet} ({niveau})...")

    plan_brut = generer_avec_groq([
        {
            "role": "system",
            "content": "Tu es un expert pédagogue pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Crée le plan d'un cours sur "{sujet}" niveau {niveau}.
Réponds UNIQUEMENT en JSON :
{{
  "titre": "...",
  "description": "description engageante de 3-4 phrases",
  "niveau": "{niveau}",
  "duree_estimee": "...",
  "objectifs": ["obj1", "obj2", "obj3", "obj4", "obj5"],
  "chapitres_prevus": [
    {{"numero": 1, "titre": "..."}},
    {{"numero": 2, "titre": "..."}},
    {{"numero": 3, "titre": "..."}},
    {{"numero": 4, "titre": "..."}},
    {{"numero": 5, "titre": "..."}}
  ]
}}"""
        }
    ], max_tokens=1000)

    return extraire_json(plan_brut)

def generer_chapitre(chapitre: dict, niveau: str) -> dict:
    print(f"  Génération chapitre {chapitre['numero']} : {chapitre['titre']}...")

    ch_brut = generer_avec_groq([
        {
            "role": "system",
            "content": "Tu es un expert pédagogue pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Génère le chapitre {chapitre['numero']} intitulé "{chapitre['titre']}"
pour un cours niveau {niveau}.
Sois très détaillé avec des exemples concrets du monde réel.
Réponds UNIQUEMENT en JSON :
{{
  "numero": {chapitre['numero']},
  "titre": "{chapitre['titre']}",
  "contenu": "explication très détaillée sur minimum 10 phrases avec des exemples",
  "points_cles": ["point 1", "point 2", "point 3", "point 4"],
  "exemple_concret": "un exemple réel et précis",
  "anecdote": "une anecdote intéressante liée au sujet",
  "quiz": [
    {{
      "question": "question de compréhension profonde ?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "bonne_reponse": "Option A",
      "explication": "explication détaillée"
    }},
    {{
      "question": "deuxième question ?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "bonne_reponse": "Option B",
      "explication": "explication détaillée"
    }}
  ],
  "exercice": {{
    "type": "pratique",
    "enonce": "description claire et motivante de l'exercice",
    "instructions": ["étape 1", "étape 2", "étape 3", "étape 4"],
    "livrable": "ce que l'apprenant doit rendre",
    "conseil": "un conseil pour réussir"
  }}
}}"""
        }
    ], max_tokens=4000)

    return extraire_json(ch_brut)

def generer_final(titre: str) -> dict:
    print("  Génération projet final et examen oral...")

    final_brut = generer_avec_groq([
        {
            "role": "system",
            "content": "Tu es un expert pédagogue pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Pour le cours "{titre}", génère le projet final et l'examen oral.
Réponds UNIQUEMENT en JSON :
{{
  "projet_final": {{
    "titre": "titre inspirant",
    "description": "description motivante sur 3-4 phrases",
    "etapes": ["étape 1", "étape 2", "étape 3", "étape 4", "étape 5"],
    "criteres_evaluation": ["critère 1", "critère 2", "critère 3", "critère 4"],
    "livrable_final": "ce que l'apprenant présente"
  }},
  "examen_oral": {{
    "questions": ["question 1", "question 2", "question 3", "question 4", "question 5"],
    "criteres_evaluation": ["clarté", "précision", "exemples concrets", "originalité"]
  }},
  "ressources": [
    {{"titre": "...", "type": "article/video/livre", "description": "pourquoi utile"}},
    {{"titre": "...", "type": "article/video/livre", "description": "pourquoi utile"}},
    {{"titre": "...", "type": "article/video/livre", "description": "pourquoi utile"}}
  ]
}}"""
        }
    ], max_tokens=2000)

    return extraire_json(final_brut)

def generer_cours_complet(sujet: str, niveau: str,
                          format_cours: str = "théorie + pratique",
                          public: str = "étudiants") -> dict:

    print(f"\nCourse Generator — {sujet}")
    print("="*50)

    # Étape 1 : Plan
    plan = generer_plan(sujet, niveau)
    print(f"Plan créé : {len(plan['chapitres_prevus'])} chapitres")

    # Étape 2 : Chapitres
    chapitres = []
    for ch in plan['chapitres_prevus']:
        try:
            chapitre = generer_chapitre(ch, niveau)
            chapitres.append(chapitre)
            print(f"  Chapitre {ch['numero']} généré — {len(chapitre['quiz'])} quiz")
        except Exception as e:
            print(f"  Erreur chapitre {ch['numero']} : {e}")
        time.sleep(1)

    # Étape 3 : Projet final + examen
    final = generer_final(plan['titre'])

    # Assemblage
    cours = {
        "titre": plan["titre"],
        "description": plan["description"],
        "niveau": plan["niveau"],
        "duree_estimee": plan["duree_estimee"],
        "objectifs": plan["objectifs"],
        "chapitres": chapitres,
        "projet_final": final["projet_final"],
        "examen_oral": final["examen_oral"],
        "ressources": final["ressources"]
    }

    # Sauvegarde
    os.makedirs("novi_ai/courses", exist_ok=True)
    chemin = f"novi_ai/courses/{sujet.lower().replace(' ', '_').replace('/', '_')}.json"
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(cours, f, ensure_ascii=False, indent=2)

    print(f"Cours sauvegardé : {chemin}")
    return cours, chemin

if __name__ == "__main__":
    cours, chemin = generer_cours_complet(
        sujet="Introduction à l'Intelligence Artificielle",
        niveau="débutant",
        format_cours="théorie + quiz + projet pratique",
        public="étudiants sans expérience en programmation"
    )
    print("\n" + "="*50)
    print("COURS GÉNÉRÉ AVEC SUCCÈS !")
    print("="*50)
    print(f"Titre     : {cours['titre']}")
    print(f"Durée     : {cours['duree_estimee']}")
    print(f"Chapitres : {len(cours['chapitres'])}")
    for ch in cours['chapitres']:
        print(f"  Chapitre {ch['numero']} : {ch['titre']}")