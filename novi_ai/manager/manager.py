import json
import os
import time
from dotenv import load_dotenv
from novi_ai.models.ai_client import appeler_ia

load_dotenv()

def generer_avec_groq(messages, max_tokens=4000):
    return appeler_ia(messages, max_tokens=max_tokens, temperature=0.3)

def extraire_json(texte: str) -> dict:
    debut = texte.find("{")
    fin = texte.rfind("}") + 1
    if debut == -1 or fin == 0:
        raise ValueError("JSON non trouvé")
    return json.loads(texte[debut:fin])

def analyser_cours(cours: dict) -> dict:
    print("Analyse du cours...")

    analyse_brut = generer_avec_groq([
        {
            "role": "system",
            "content": "Tu es un expert en qualité pédagogique pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Analyse ce cours et identifie tous les problèmes de qualité.
Cours à analyser :
{json.dumps(cours, ensure_ascii=False, indent=2)}

Réponds UNIQUEMENT en JSON :
{{
  "score_global": 0-100,
  "niveau_adapte": true,
  "problemes": [
    {{
      "type": "contenu/quiz/exercice/structure",
      "chapitre": 1,
      "description": "description précise du problème",
      "severite": "faible/moyenne/haute"
    }}
  ],
  "points_forts": ["point fort 1", "point fort 2"],
  "recommandations": ["recommandation 1", "recommandation 2"],
  "pret_pour_publication": true
}}"""
        }
    ], max_tokens=2000)

    return extraire_json(analyse_brut)

def ameliorer_chapitre(chapitre: dict, problemes: list, niveau: str) -> dict:
    problemes_chapitre = [
        p for p in problemes
        if p.get("chapitre") == chapitre["numero"]
    ]

    if not problemes_chapitre:
        print(f"  Chapitre {chapitre['numero']} — aucun problème, conservé tel quel")
        return chapitre

    print(f"  Chapitre {chapitre['numero']} — {len(problemes_chapitre)} problème(s) à corriger...")

    ameliore_brut = generer_avec_groq([
        {
            "role": "system",
            "content": "Tu es un expert pédagogue pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Améliore ce chapitre en corrigeant les problèmes identifiés.
Niveau du cours : {niveau}

Chapitre actuel :
{json.dumps(chapitre, ensure_ascii=False, indent=2)}

Problèmes à corriger :
{json.dumps(problemes_chapitre, ensure_ascii=False, indent=2)}

Retourne le chapitre complet amélioré en JSON avec exactement la même structure."""
        }
    ], max_tokens=4000)

    try:
        return extraire_json(ameliore_brut)
    except Exception as e:
        print(f"  Erreur amélioration chapitre {chapitre['numero']} : {e}")
        return chapitre

def valider_cours(cours: dict) -> dict:
    print("Validation finale du cours...")

    validation_brut = generer_avec_groq([
        {
            "role": "system",
            "content": "Tu es un expert en certification pédagogique pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Fais la validation finale de ce cours.
Cours :
{json.dumps(cours, ensure_ascii=False, indent=2)}

Réponds UNIQUEMENT en JSON :
{{
  "score_final": 0-100,
  "certification_novi": true,
  "niveau_confirme": "débutant/intermédiaire/avancé",
  "duree_confirmee": "...",
  "points_forts_finaux": ["point 1", "point 2", "point 3"],
  "certification": {{
    "titre": "Certificat NOVI Académie",
    "mention": "Passable/Bien/Très Bien/Excellent",
    "competences_certifiees": ["compétence 1", "compétence 2", "compétence 3"],
    "valide_pour": "2 ans",
    "delivrable": "Certificat numérique NOVI + attestation PDF"
  }},
  "commentaire_final": "commentaire encourageant pour l'apprenant"
}}""" 
        }
    ], max_tokens=1000)

    return extraire_json(validation_brut)

def gerer_cours(chemin_cours: str) -> dict:
    with open(chemin_cours, "r", encoding="utf-8") as f:
        cours = json.load(f)

    print(f"\nCourse Manager — {cours['titre']}")
    print("="*50)

    # Étape 1 : Analyser
    analyse = analyser_cours(cours)
    print(f"Score initial    : {analyse['score_global']}/100")
    print(f"Problèmes        : {len(analyse['problemes'])}")

    if analyse['problemes']:
        print("Problèmes détectés :")
        for p in analyse['problemes']:
            print(f"  [{p['severite'].upper()}] Chapitre {p.get('chapitre', '?')} — {p['description']}")

    # Étape 2 : Améliorer
    print("\nAmélioration des chapitres...")
    chapitres_ameliores = []
    for chapitre in cours["chapitres"]:
        chapitre_ameliore = ameliorer_chapitre(
            chapitre,
            analyse["problemes"],
            cours["niveau"]
        )
        chapitres_ameliores.append(chapitre_ameliore)
        time.sleep(1)

    cours["chapitres"] = chapitres_ameliores

    # Étape 3 : Valider
    validation = valider_cours(cours)
    print(f"Score final      : {validation['score_final']}/100")
    print(f"Badge qualité    : {validation.get('badge_qualite', 'N/A')}")
    print(f"Certification    : {validation['certification_novi']}")

    # Assemblage final
    cours_final = {
        **cours,
        "qualite": {
            "score_initial": analyse["score_global"],
            "score_final": validation["score_final"],
            "badge": validation.get("badge_qualite", "Bien"),
            "certification_novi": validation["certification_novi"],
            "points_forts": validation["points_forts_finaux"],
            "commentaire": validation["commentaire_final"]
        }
    }

    # Sauvegarde
    chemin_final = chemin_cours.replace(".json", "_valide.json")
    with open(chemin_final, "w", encoding="utf-8") as f:
        json.dump(cours_final, f, ensure_ascii=False, indent=2)

    print(f"Cours validé sauvegardé : {chemin_final}")
    return cours_final

if __name__ == "__main__":
    cours_final = gerer_cours("novi_ai/courses/introduction_à_l'intelligence_artificielle.json")

    print("\n" + "="*50)
    print("COURSE MANAGER TERMINÉ !")
    print("="*50)
    print(f"Titre     : {cours_final['titre']}")
    print(f"Score     : {cours_final['qualite']['score_final']}/100")
    print(f"Badge     : {cours_final['qualite']['badge']}")
    print(f"Certifié  : {cours_final['qualite']['certification_novi']}")
    print(f"Commentaire : {cours_final['qualite']['commentaire']}")