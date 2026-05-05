import json
import os
import time
from dotenv import load_dotenv
from novi_ai.models.ai_client import appeler_ia
from novi_ai.manager.manager import gerer_cours

load_dotenv()

def extraire_json(texte: str) -> dict:
    debut = texte.find("{")
    fin = texte.rfind("}") + 1
    if debut == -1 or fin == 0:
        raise ValueError("JSON non trouvé")
    return json.loads(texte[debut:fin])

CATALOGUE = [
    {
        "sujet": "Introduction à l'Intelligence Artificielle",
        "niveau": "débutant",
        "domaine": "IA",
        "public": "étudiants sans expérience"
    },
    {
        "sujet": "Python pour la Data Science",
        "niveau": "débutant",
        "domaine": "Programmation",
        "public": "étudiants en informatique"
    },
    {
        "sujet": "Introduction à l'IOT",
        "niveau": "débutant",
        "domaine": "IOT",
        "public": "ingénieurs débutants"
    },
    {
        "sujet": "Machine Learning Avancé",
        "niveau": "intermédiaire",
        "domaine": "IA",
        "public": "développeurs avec bases en Python"
    },
    {
        "sujet": "Robotique et Automatisation",
        "niveau": "intermédiaire",
        "domaine": "Robotique",
        "public": "ingénieurs en automatisation"
    },
    {
        "sujet": "Droit du Numérique",
        "niveau": "débutant",
        "domaine": "Juridique",
        "public": "professionnels de la tech"
    },
    {
        "sujet": "Anglais Technique pour la Tech",
        "niveau": "débutant",
        "domaine": "Langue",
        "public": "professionnels francophones"
    },
    {
        "sujet": "Cybersécurité et Protection des Données",
        "niveau": "intermédiaire",
        "domaine": "Sécurité",
        "public": "développeurs et administrateurs"
    }
]

def nettoyer_nom(texte: str) -> str:
    """Convertit un titre en nom de fichier propre"""
    nom = texte.lower()
    remplacements = {
        " ": "_", "'": "", "é": "e", "è": "e", "ê": "e",
        "à": "a", "ô": "o", "î": "i", "ù": "u", "ç": "c",
        ",": "", ":": "", "!": "", "?": "", "&": "et"
    }
    for ancien, nouveau in remplacements.items():
        nom = nom.replace(ancien, nouveau)
    return nom[:60]

def generer_plan(sujet: str, niveau: str, public: str) -> dict:
    plan_brut = appeler_ia([
        {
            "role": "system",
            "content": "Tu es un expert pédagogue pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Crée le plan d'un cours sur "{sujet}" niveau {niveau} pour {public}.
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
    ch_brut = appeler_ia([
        {
            "role": "system",
            "content": "Tu es un expert pédagogue pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Génère le chapitre {chapitre['numero']} : "{chapitre['titre']}" niveau {niveau}.
Réponds UNIQUEMENT en JSON :
{{
  "numero": {chapitre['numero']},
  "titre": "{chapitre['titre']}",
  "contenu": "explication très détaillée minimum 10 phrases",
  "points_cles": ["point 1", "point 2", "point 3", "point 4"],
  "exemple_concret": "exemple réel et précis",
  "anecdote": "anecdote intéressante",
  "quiz": [
    {{
      "question": "question de compréhension ?",
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
    "enonce": "description claire de l'exercice",
    "instructions": ["étape 1", "étape 2", "étape 3", "étape 4"],
    "livrable": "ce que l'apprenant doit rendre",
    "conseil": "conseil pour réussir"
  }}
}}"""
        }
    ], max_tokens=4000)
    return extraire_json(ch_brut)

def generer_final(titre: str) -> dict:
    final_brut = appeler_ia([
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
    "criteres_evaluation": ["critère 1", "critère 2", "critère 3"],
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

def generer_et_valider_cours(item: dict) -> tuple:
    print(f"\n{'='*50}")
    print(f"Génération : {item['sujet']}")
    print(f"{'='*50}")

    os.makedirs("novi_ai/courses", exist_ok=True)
    nom_fichier = nettoyer_nom(item['sujet'])
    chemin = f"novi_ai/courses/{nom_fichier}.json"

    # Vérifier si le cours validé existe déjà
    chemin_valide = chemin.replace(".json", "_valide.json")
    if os.path.exists(chemin_valide):
        print(f"Cours déjà validé — ignoré")
        return None, chemin_valide

    # Générer le plan
    plan = generer_plan(item['sujet'], item['niveau'], item['public'])
    print(f"Plan créé : {len(plan['chapitres_prevus'])} chapitres")

    # Générer les chapitres
    chapitres = []
    for ch in plan['chapitres_prevus']:
        print(f"  Chapitre {ch['numero']} : {ch['titre']}...")
        try:
            chapitre = generer_chapitre(ch, item['niveau'])
            chapitres.append(chapitre)
            print(f"  ✓ Chapitre {ch['numero']} généré")
        except Exception as e:
            print(f"  ✗ Erreur chapitre {ch['numero']} : {e}")
        time.sleep(2)

    # Générer le projet final
    final = generer_final(plan['titre'])

    cours = {
        "titre": plan["titre"],
        "description": plan["description"],
        "niveau": plan["niveau"],
        "domaine": item["domaine"],
        "duree_estimee": plan["duree_estimee"],
        "objectifs": plan["objectifs"],
        "chapitres": chapitres,
        "projet_final": final["projet_final"],
        "examen_oral": final["examen_oral"],
        "ressources": final["ressources"]
    }

    # Sauvegarder le cours brut
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(cours, f, ensure_ascii=False, indent=2)
    print(f"Cours sauvegardé : {chemin}")

    # Valider avec le Course Manager
    print("Course Manager — validation en cours...")
    try:
        cours_valide = gerer_cours(chemin)
        print(f"✓ Validé — Score : {cours_valide['qualite']['score_final']}/100")
        print(f"  Badge : {cours_valide['qualite']['badge']}")
        print(f"  Certifié : {cours_valide['qualite']['certification_novi']}")
        return cours_valide, chemin_valide
    except Exception as e:
        print(f"✗ Erreur validation : {e}")
        return cours, chemin

if __name__ == "__main__":
    print("NOVI — Génération et validation du catalogue")
    print(f"Cours à générer : {len(CATALOGUE)}")

    resultats = []

    for i, item in enumerate(CATALOGUE):
        print(f"\nCours {i+1}/{len(CATALOGUE)}")
        try:
            cours, chemin = generer_et_valider_cours(item)
            if cours:
                resultats.append({
                    "titre": cours.get("titre", item["sujet"]),
                    "chemin": chemin,
                    "score": cours.get("qualite", {}).get("score_final", "N/A")
                })
        except Exception as e:
            print(f"Erreur : {e}")

        if i < len(CATALOGUE) - 1:
            print(f"\nPause 30 secondes avant le prochain cours...")
            time.sleep(30)

    print(f"\n{'='*50}")
    print(f"CATALOGUE TERMINÉ : {len(resultats)} cours générés et validés")
    print(f"{'='*50}")
    for r in resultats:
        print(f"  ✓ {r['titre']} — Score {r['score']}/100")