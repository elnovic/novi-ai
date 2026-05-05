import os
import json
import requests
from dotenv import load_dotenv
from novi_ai.models.ai_client import appeler_ia

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

PAYS_CONFIG = {
    "Maroc": {
        "drapeau": "🇲🇦",
        "lat": 31.7917,
        "lng": -7.0926,
        "score": 78,
        "mots_cles": ["Morocco AI", "Maroc technologie", "Morocco startup", "Morocco innovation"],
        "langue": "fr"
    },
    "Sénégal": {
        "drapeau": "🇸🇳",
        "lat": 14.4974,
        "lng": -14.4524,
        "score": 65,
        "mots_cles": ["Senegal tech", "Sénégal numérique", "Dakar startup"],
        "langue": "fr"
    },
    "France": {
        "drapeau": "🇫🇷",
        "lat": 46.2276,
        "lng": 2.2137,
        "score": 92,
        "mots_cles": ["France IA", "French AI startup", "France technologie", "Mistral AI"],
        "langue": "fr"
    },
    "Nigeria": {
        "drapeau": "🇳🇬",
        "lat": 9.0820,
        "lng": 8.6753,
        "score": 71,
        "mots_cles": ["Nigeria tech", "Lagos startup", "Nigeria AI", "Nigeria fintech"],
        "langue": "en"
    },
    "USA": {
        "drapeau": "🇺🇸",
        "lat": 37.0902,
        "lng": -95.7129,
        "score": 99,
        "mots_cles": ["OpenAI", "artificial intelligence", "Silicon Valley", "US tech"],
        "langue": "en"
    },
    "Chine": {
        "drapeau": "🇨🇳",
        "lat": 35.8617,
        "lng": 104.1954,
        "score": 97,
        "mots_cles": ["China AI", "Chinese technology", "DeepSeek", "Baidu AI"],
        "langue": "en"
    },
    "Allemagne": {
        "drapeau": "🇩🇪",
        "lat": 51.1657,
        "lng": 10.4515,
        "score": 94,
        "mots_cles": ["Germany AI", "Deutsche Telekom", "German startup", "BMW autonomous"],
        "langue": "en"
    },
    "Inde": {
        "drapeau": "🇮🇳",
        "lat": 20.5937,
        "lng": 78.9629,
        "score": 85,
        "mots_cles": ["India AI", "Indian startup", "Bangalore tech", "India technology"],
        "langue": "en"
    },
    "Rwanda": {
        "drapeau": "🇷🇼",
        "lat": -1.9403,
        "lng": 29.8739,
        "score": 74,
        "mots_cles": ["Rwanda tech", "Kigali innovation", "Rwanda drone", "Rwanda digital"],
        "langue": "en"
    },
    "Japon": {
        "drapeau": "🇯🇵",
        "lat": 36.2048,
        "lng": 138.2529,
        "score": 91,
        "mots_cles": ["Japan AI", "Japan robotics", "Sony AI", "Japan technology"],
        "langue": "en"
    }
}

def recuperer_actualites(pays: str, config: dict) -> list:
    """Récupère les actualités tech d'un pays via NewsAPI"""
    articles = []

    for mot_cle in config["mots_cles"][:2]:  # 2 mots-clés par pays
        try:
            params = {
                "q": mot_cle,
                "language": config["langue"],
                "sortBy": "publishedAt",
                "pageSize": 3,
                "apiKey": NEWS_API_KEY
            }
            response = requests.get(NEWS_API_URL, params=params, timeout=10)
            data = response.json()

            if data.get("status") == "ok":
                for article in data.get("articles", []):
                    if article.get("title") and article.get("description"):
                        articles.append({
                            "titre": article["title"],
                            "description": article["description"],
                            "source": article["source"]["name"],
                            "url": article["url"],
                            "date": article["publishedAt"][:10]
                        })
        except Exception as e:
            print(f"Erreur NewsAPI pour {pays} : {e}")

    return articles[:5]  # Max 5 articles par pays

def analyser_tendances(pays: str, articles: list) -> dict:
    """Utilise l'IA pour analyser les tendances depuis les articles"""
    if not articles:
        return {
            "tendances": ["Données en cours de chargement"],
            "resume": "Actualités en cours de récupération."
        }

    articles_texte = "\n".join([
        f"- {a['titre']}: {a['description']}"
        for a in articles[:5]
    ])

    analyse_brut = appeler_ia([
        {
            "role": "system",
            "content": "Tu es un expert en veille technologique. Tu réponds UNIQUEMENT en JSON valide."
        },
        {
            "role": "user",
            "content": f"""Analyse ces actualités tech de {pays} et extrais les tendances principales.

Articles :
{articles_texte}

Réponds UNIQUEMENT en JSON :
{{
  "tendances": ["tendance 1", "tendance 2", "tendance 3"],
  "resume": "résumé de 2-3 phrases de la situation tech de ce pays"
}}"""
        }
    ], max_tokens=500, temperature=0.3)

    try:
        debut = analyse_brut.find("{")
        fin = analyse_brut.rfind("}") + 1
        return json.loads(analyse_brut[debut:fin])
    except:
        return {
            "tendances": ["Innovation technologique", "Développement numérique"],
            "resume": "Ce pays développe activement son écosystème technologique."
        }

def generer_donnees_innovation() -> dict:
    """Génère les données complètes pour Novi Innovation"""
    print("NOVI Innovation — Génération des données en temps réel")
    print("="*50)

    donnees = {}

    for pays, config in PAYS_CONFIG.items():
        print(f"\nTraitement : {pays} {config['drapeau']}")

        # Récupérer les actualités
        articles = recuperer_actualites(pays, config)
        print(f"  Articles trouvés : {len(articles)}")

        # Analyser les tendances avec l'IA
        if articles:
            analyse = analyser_tendances(pays, articles)
        else:
            analyse = {
                "tendances": ["Innovation en cours", "Développement tech"],
                "resume": "Données en cours de mise à jour."
            }

        donnees[pays] = {
            "drapeau": config["drapeau"],
            "lat": config["lat"],
            "lng": config["lng"],
            "score": config["score"],
            "tendances": analyse["tendances"],
            "resume": analyse["resume"],
            "actualites": articles,
            "startups": get_startups_count(pays),
            "investissement": get_investissement(pays),
            "universites_tech": get_universites(pays)
        }

        print(f"  Tendances : {', '.join(analyse['tendances'][:2])}")

    return donnees

def get_startups_count(pays: str) -> str:
    counts = {
        "Maroc": "340+", "Sénégal": "180+", "France": "4 200+",
        "Nigeria": "890+", "USA": "45 000+", "Chine": "12 000+",
        "Allemagne": "3 800+", "Inde": "11 000+", "Rwanda": "120+",
        "Japon": "5 600+"
    }
    return counts.get(pays, "100+")

def get_investissement(pays: str) -> str:
    investments = {
        "Maroc": "2.1 Mds $", "Sénégal": "450 M $", "France": "12.4 Mds $",
        "Nigeria": "3.2 Mds $", "USA": "340 Mds $", "Chine": "95 Mds $",
        "Allemagne": "18.7 Mds $", "Inde": "28 Mds $", "Rwanda": "280 M $",
        "Japon": "15.3 Mds $"
    }
    return investments.get(pays, "N/A")

def get_universites(pays: str) -> int:
    universites = {
        "Maroc": 12, "Sénégal": 8, "France": 45,
        "Nigeria": 22, "USA": 320, "Chine": 180,
        "Allemagne": 67, "Inde": 95, "Rwanda": 5,
        "Japon": 48
    }
    return universites.get(pays, 5)

if __name__ == "__main__":
    donnees = generer_donnees_innovation()

    # Sauvegarder
    with open("innovation_data.json", "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Données générées pour {len(donnees)} pays")
    print("Fichier sauvegardé : innovation_data.json")