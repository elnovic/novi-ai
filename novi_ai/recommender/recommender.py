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

CATALOGUE_COURS = [
    {
        "id": "cours_001",
        "titre": "Introduction à l'Intelligence Artificielle",
        "niveau": "débutant",
        "duree": "12 heures",
        "domaine": "IA",
        "prerequis": [],
        "competences_acquises": ["bases IA", "machine learning", "deep learning"],
        "badge": "Or",
        "score_qualite": 95
    },
    {
        "id": "cours_002",
        "titre": "Python pour la Data Science",
        "niveau": "débutant",
        "duree": "10 heures",
        "domaine": "Programmation",
        "prerequis": [],
        "competences_acquises": ["python", "pandas", "numpy", "visualisation"],
        "badge": "Argent",
        "score_qualite": 88
    },
    {
        "id": "cours_003",
        "titre": "Machine Learning Avancé",
        "niveau": "intermédiaire",
        "duree": "20 heures",
        "domaine": "IA",
        "prerequis": ["bases IA", "python"],
        "competences_acquises": ["réseaux de neurones", "CNN", "RNN", "transformers"],
        "badge": "Or",
        "score_qualite": 92
    },
    {
        "id": "cours_004",
        "titre": "Introduction à l'IOT",
        "niveau": "débutant",
        "duree": "8 heures",
        "domaine": "IOT",
        "prerequis": [],
        "competences_acquises": ["capteurs", "arduino", "raspberry pi", "protocoles IOT"],
        "badge": "Argent",
        "score_qualite": 86
    },
    {
        "id": "cours_005",
        "titre": "Robotique et Automatisation",
        "niveau": "intermédiaire",
        "duree": "15 heures",
        "domaine": "Robotique",
        "prerequis": ["python", "capteurs"],
        "competences_acquises": ["ros", "contrôle moteur", "vision artificielle"],
        "badge": "Or",
        "score_qualite": 90
    },
    {
        "id": "cours_006",
        "titre": "Droit du Numérique",
        "niveau": "débutant",
        "duree": "6 heures",
        "domaine": "Juridique",
        "prerequis": [],
        "competences_acquises": ["rgpd", "propriété intellectuelle", "cybersécurité juridique"],
        "badge": "Argent",
        "score_qualite": 84
    },
    {
        "id": "cours_007",
        "titre": "Anglais Technique pour la Tech",
        "niveau": "débutant",
        "duree": "8 heures",
        "domaine": "Langue",
        "prerequis": [],
        "competences_acquises": ["vocabulaire tech", "lecture documentation", "communication"],
        "badge": "Argent",
        "score_qualite": 87
    }
]

def analyser_profil(profil: dict) -> dict:
    print("Analyse du profil apprenant...")

    analyse_brut = generer_avec_groq([
        {
            "role": "system",
            "content": "Tu es un conseiller pédagogique expert pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Analyse ce profil d'apprenant et identifie ses besoins.
Profil :
{json.dumps(profil, ensure_ascii=False, indent=2)}

Réponds UNIQUEMENT en JSON :
{{
  "niveau_detecte": "débutant/intermédiaire/avancé",
  "domaines_prioritaires": ["domaine 1", "domaine 2", "domaine 3"],
  "competences_actuelles": ["compétence 1", "compétence 2"],
  "competences_manquantes": ["compétence 1", "compétence 2"],
  "objectif_principal": "description de l'objectif principal",
  "temps_disponible_semaine": "X heures",
  "style_apprentissage": "pratique/théorique/mixte"
}}"""
        }
    ], max_tokens=1000)

    return extraire_json(analyse_brut)

def selectionner_cours(profil: dict, analyse: dict) -> dict:
    print("Sélection des cours adaptés...")

    selection_brut = generer_avec_groq([
        {
            "role": "system",
            "content": "Tu es un conseiller pédagogique expert pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Sur la base du profil et du catalogue, sélectionne les meilleurs cours.

Profil apprenant :
{json.dumps(profil, ensure_ascii=False, indent=2)}

Analyse du profil :
{json.dumps(analyse, ensure_ascii=False, indent=2)}

Catalogue disponible :
{json.dumps(CATALOGUE_COURS, ensure_ascii=False, indent=2)}

Réponds UNIQUEMENT en JSON :
{{
  "cours_recommandes": [
    {{
      "id": "cours_xxx",
      "titre": "...",
      "raison": "pourquoi ce cours est recommandé",
      "priorite": 1,
      "duree_adaptee": "..."
    }}
  ],
  "cours_a_eviter": [
    {{
      "id": "cours_xxx",
      "raison": "pourquoi ce cours n'est pas adapté maintenant"
    }}
  ]
}}"""
        }
    ], max_tokens=2000)

    return extraire_json(selection_brut)

def generer_parcours(profil: dict, analyse: dict, selection: dict) -> dict:
    print("Génération du parcours personnalisé...")

    parcours_brut = generer_avec_groq([
        {
            "role": "system",
            "content": "Tu es un conseiller pédagogique expert pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Crée un parcours d'apprentissage personnalisé complet.

Profil apprenant :
{json.dumps(profil, ensure_ascii=False, indent=2)}

Analyse :
{json.dumps(analyse, ensure_ascii=False, indent=2)}

Cours sélectionnés :
{json.dumps(selection, ensure_ascii=False, indent=2)}

Réponds UNIQUEMENT en JSON :
{{
  "nom_parcours": "nom inspirant du parcours",
  "description": "description motivante du parcours",
  "duree_totale": "X semaines",
  "objectif_final": "ce que l'apprenant sera capable de faire",
  "etapes": [
    {{
      "semaine": 1,
      "cours_id": "cours_xxx",
      "titre_cours": "...",
      "objectif_semaine": "ce qu'on apprend cette semaine",
      "heures_par_jour": 2,
      "conseil_motivation": "conseil personnalisé"
    }}
  ],
  "jalons": [
    {{
      "semaine": 2,
      "titre": "nom du jalon",
      "description": "ce que l'apprenant a accompli",
      "badge_debloque": "nom du badge"
    }}
  ],
  "message_personnalise": "message d'encouragement personnalisé"
}}"""
        }
    ], max_tokens=3000)

    return extraire_json(parcours_brut)

def recommander(profil: dict) -> dict:
    print(f"\nRecommendation Engine — {profil['nom']}")
    print("="*50)

    analyse = analyser_profil(profil)
    print(f"Niveau détecté        : {analyse['niveau_detecte']}")
    print(f"Domaines prioritaires : {', '.join(analyse['domaines_prioritaires'])}")
    print(f"Objectif              : {analyse['objectif_principal']}")

    time.sleep(1)

    selection = selectionner_cours(profil, analyse)
    print(f"\nCours recommandés : {len(selection['cours_recommandes'])}")
    for c in selection['cours_recommandes']:
        print(f"  {c['priorite']}. {c['titre']}")
        print(f"     Raison : {c['raison'][:70]}...")

    time.sleep(1)

    parcours = generer_parcours(profil, analyse, selection)
    print(f"\nParcours : {parcours['nom_parcours']}")
    print(f"Durée    : {parcours['duree_totale']}")
    print(f"Étapes   : {len(parcours['etapes'])} semaines")

    resultat = {
        "profil": profil,
        "analyse": analyse,
        "selection": selection,
        "parcours": parcours
    }

    nom_fichier = f"parcours_{profil['nom'].lower().replace(' ', '_')}.json"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(resultat, f, ensure_ascii=False, indent=2)

    print(f"Parcours sauvegardé : {nom_fichier}")
    return resultat

if __name__ == "__main__":
    profil_test = {
        "nom": "Amadou Diallo",
        "age": 22,
        "niveau_actuel": "débutant",
        "formation_actuelle": "Licence en informatique",
        "objectifs": [
            "Travailler dans l'IA",
            "Créer des projets concrets",
            "Obtenir des certifications"
        ],
        "domaines_interets": ["IA", "Robotique", "IOT"],
        "cours_deja_suivis": [],
        "temps_disponible": "2 heures par jour",
        "style_prefere": "pratique avec des projets"
    }

    resultat = recommander(profil_test)

    print("\n" + "="*50)
    print("RECOMMENDATION ENGINE TERMINÉ !")
    print("="*50)
    print(f"Parcours       : {resultat['parcours']['nom_parcours']}")
    print(f"Durée totale   : {resultat['parcours']['duree_totale']}")
    print(f"Objectif final : {resultat['parcours']['objectif_final']}")
    print(f"Message        : {resultat['parcours']['message_personnalise']}")