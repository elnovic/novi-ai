def build_course_prompt(sujet: str, niveau: str, format_cours: str, public: str) -> str:
    return f"""Tu es un expert pédagogue spécialisé en technologie pour la plateforme NOVI Académie.
Ta mission est de créer un cours complet, structuré et de haute qualité.

INFORMATIONS DU COURS :
- Sujet : {sujet}
- Niveau : {niveau}
- Format : {format_cours}
- Public cible : {public}

INSTRUCTIONS STRICTES :
1. Le cours doit être professionnel et engageant
2. Chaque chapitre doit avoir un contenu clair et des exemples concrets
3. Les quiz doivent tester la compréhension réelle, pas la mémorisation
4. Les exercices pratiques doivent être réalisables par le public cible
5. Tu dois répondre UNIQUEMENT en JSON valide, sans texte avant ou après

STRUCTURE JSON OBLIGATOIRE :
{{
  "titre": "titre du cours",
  "description": "description courte et engageante",
  "niveau": "{niveau}",
  "duree_estimee": "Xh",
  "objectifs": ["objectif 1", "objectif 2", "objectif 3"],
  "chapitres": [
    {{
      "numero": 1,
      "titre": "titre du chapitre",
      "contenu": "explication détaillée du chapitre",
      "points_cles": ["point 1", "point 2"],
      "exemple_concret": "un exemple réel et pratique",
      "quiz": [
        {{
          "question": "question du quiz",
          "options": ["option A", "option B", "option C", "option D"],
          "bonne_reponse": "option A",
          "explication": "pourquoi c'est la bonne réponse"
        }}
      ],
      "exercice": {{
        "type": "pratique",
        "enonce": "description de l'exercice",
        "instructions": ["étape 1", "étape 2", "étape 3"],
        "livrable": "ce que l'apprenant doit rendre"
      }}
    }}
  ],
  "projet_final": {{
    "titre": "titre du projet",
    "description": "description du projet final",
    "etapes": ["étape 1", "étape 2", "étape 3"],
    "criteres_evaluation": ["critère 1", "critère 2"]
  }},
  "examen_oral": {{
    "questions": ["question 1", "question 2", "question 3"],
    "criteres_evaluation": ["clarté", "précision", "exemples donnés"]
  }},
  "ressources": [
    {{
      "titre": "titre de la ressource",
      "type": "article/video/livre",
      "description": "pourquoi cette ressource est utile"
    }}
  ]
}}

Génère maintenant le cours complet en JSON :"""