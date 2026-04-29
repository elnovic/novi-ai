import json
import os
import time
from dotenv import load_dotenv
from novi_ai.models.ai_client import appeler_ia
from novi_ai.manager.manager import gerer_cours
from novi_ai.recommender.recommender import recommander

load_dotenv()

def extraire_json(texte: str) -> dict:
    debut = texte.find("{")
    fin = texte.rfind("}") + 1
    if debut == -1 or fin == 0:
        raise ValueError("JSON non trouvé")
    return json.loads(texte[debut:fin])

def pipeline_complet(sujet: str, niveau: str, profil_apprenant: dict):
    print("\n" + "="*60)
    print("NOVI AI ENGINE — PIPELINE COMPLET")
    print("="*60)

    # ─────────────────────────────────────────
    # MODULE 1 : Course Generator
    # ─────────────────────────────────────────
    print("\nMODULE 1 — Course Generator")
    print("-"*40)

    # Générer le plan
    plan_brut = appeler_ia([
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

    plan = extraire_json(plan_brut)
    print(f"Cours : {plan['titre']}")
    print(f"Chapitres prévus : {len(plan['chapitres_prevus'])}")

    # Générer les chapitres
    chapitres = []
    for ch in plan['chapitres_prevus']:
        print(f"  Génération chapitre {ch['numero']} : {ch['titre']}...")
        ch_brut = appeler_ia([
            {
                "role": "system",
                "content": "Tu es un expert pédagogue pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
            },
            {
                "role": "user",
                "content": f"""Génère le chapitre {ch['numero']} : "{ch['titre']}" pour un cours {niveau}.
Réponds UNIQUEMENT en JSON :
{{
  "numero": {ch['numero']},
  "titre": "{ch['titre']}",
  "contenu": "explication détaillée minimum 10 phrases",
  "points_cles": ["point 1", "point 2", "point 3", "point 4"],
  "exemple_concret": "exemple réel et précis",
  "anecdote": "anecdote intéressante",
  "quiz": [
    {{
      "question": "question ?",
      "options": ["A", "B", "C", "D"],
      "bonne_reponse": "A",
      "explication": "explication"
    }},
    {{
      "question": "question 2 ?",
      "options": ["A", "B", "C", "D"],
      "bonne_reponse": "B",
      "explication": "explication"
    }}
  ],
  "exercice": {{
    "type": "pratique",
    "enonce": "description de l'exercice",
    "instructions": ["étape 1", "étape 2", "étape 3", "étape 4"],
    "livrable": "ce que l'apprenant rend",
    "conseil": "conseil pour réussir"
  }}
}}"""
            }
        ], max_tokens=4000)

        try:
            chapitre = extraire_json(ch_brut)
            chapitres.append(chapitre)
            print(f"  Chapitre {ch['numero']} généré — {len(chapitre['quiz'])} quiz")
        except Exception as e:
            print(f"  Erreur chapitre {ch['numero']} : {e}")
        time.sleep(1)

    # Générer projet final + examen oral
    final_brut = appeler_ia([
        {
            "role": "system",
            "content": "Tu es un expert pédagogue pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Pour le cours "{plan['titre']}", génère le projet final et l'examen oral.
Réponds UNIQUEMENT en JSON :
{{
  "projet_final": {{
    "titre": "...",
    "description": "...",
    "etapes": ["étape 1", "étape 2", "étape 3", "étape 4", "étape 5"],
    "criteres_evaluation": ["critère 1", "critère 2", "critère 3"],
    "livrable_final": "..."
  }},
  "examen_oral": {{
    "questions": ["q1", "q2", "q3", "q4", "q5"],
    "criteres_evaluation": ["clarté", "précision", "exemples", "originalité"]
  }},
  "ressources": [
    {{"titre": "...", "type": "article/video/livre", "description": "..."}},
    {{"titre": "...", "type": "article/video/livre", "description": "..."}},
    {{"titre": "...", "type": "article/video/livre", "description": "..."}}
  ]
}}"""
        }
    ], max_tokens=2000)

    final = extraire_json(final_brut)

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

    os.makedirs("novi_ai/courses", exist_ok=True)
    chemin_cours = f"novi_ai/courses/{sujet.lower().replace(' ', '_').replace('/', '_')}.json"
    with open(chemin_cours, "w", encoding="utf-8") as f:
        json.dump(cours, f, ensure_ascii=False, indent=2)
    print(f"Cours sauvegardé : {chemin_cours}")

    # ─────────────────────────────────────────
    # MODULE 2 : Course Manager
    # ─────────────────────────────────────────
    print("\nMODULE 2 — Course Manager")
    print("-"*40)
    cours_valide = gerer_cours(chemin_cours)

    # ─────────────────────────────────────────
    # MODULE 3 : Recommendation Engine
    # ─────────────────────────────────────────
    print("\nMODULE 3 — Recommendation Engine")
    print("-"*40)
    resultat = recommander(profil_apprenant)

    # ─────────────────────────────────────────
    # RÉSUMÉ FINAL
    # ─────────────────────────────────────────
    print("\n" + "="*60)
    print("NOVI AI ENGINE — RÉSUMÉ FINAL")
    print("="*60)
    print(f"Cours généré     : {cours_valide['titre']}")
    print(f"Score qualité    : {cours_valide['qualite']['score_final']}/100")
    print(f"Badge            : {cours_valide['qualite']['badge']}")
    print(f"Certifié NOVI    : {cours_valide['qualite']['certification_novi']}")
    print(f"Chapitres        : {len(cours_valide['chapitres'])}")
    print()
    print(f"Apprenant        : {profil_apprenant['nom']}")
    print(f"Parcours         : {resultat['parcours']['nom_parcours']}")
    print(f"Durée parcours   : {resultat['parcours']['duree_totale']}")
    print(f"Objectif final   : {resultat['parcours']['objectif_final']}")
    print("="*60)
    print("NOVI AI ENGINE OPÉRATIONNEL !")
    print("="*60)

if __name__ == "__main__":
    pipeline_complet(
        sujet="Introduction à l'Intelligence Artificielle",
        niveau="débutant",
        profil_apprenant={
            "nom": "Amadou Diallo",
            "age": 22,
            "niveau_actuel": "débutant",
            "formation_actuelle": "Licence en informatique",
            "objectifs": ["Travailler dans l'IA", "Créer des projets concrets"],
            "domaines_interets": ["IA", "Robotique", "IOT"],
            "cours_deja_suivis": [],
            "temps_disponible": "2 heures par jour",
            "style_prefere": "pratique avec des projets"
        }
    )