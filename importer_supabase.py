import json
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Connexion Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def importer_cours(chemin_fichier: str):
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        cours = json.load(f)

    # Générer un ID propre
    cours_id = cours["titre"].lower()
    cours_id = cours_id.replace(" ", "_")
    cours_id = cours_id.replace("'", "")
    cours_id = cours_id.replace("é", "e")
    cours_id = cours_id.replace("è", "e")
    cours_id = cours_id.replace("ê", "e")
    cours_id = cours_id.replace("à", "a")
    cours_id = cours_id.replace("ô", "o")
    cours_id = cours_id.replace("î", "i")
    cours_id = cours_id.replace(",", "")
    cours_id = cours_id.replace(":", "")
    cours_id = cours_id[:50]

    print(f"Import : {cours['titre']}")
    print(f"ID     : {cours_id}")

    data = {
        "id": cours_id,
        "titre": cours["titre"],
        "description": cours.get("description", ""),
        "niveau": cours.get("niveau", "débutant"),
        "domaine": cours.get("domaine", "IA"),
        "duree_estimee": cours.get("duree_estimee", "10 heures"),
        "score_qualite": cours.get("qualite", {}).get("score_final", 85),
        "certification": cours.get("qualite", {}).get("certification_novi", True),
        "contenu": cours
    }

    result = supabase.table("cours").upsert(data).execute()
    print(f"Importé avec succès — Score : {data['score_qualite']}/100")
    return cours_id

def importer_tous_les_cours():
    dossier = "novi_ai/courses"
    fichiers = os.listdir(dossier)

    # Prendre les fichiers validés en priorité
    # Sinon prendre les fichiers normaux si pas de version validée
    fichiers_valides = [f for f in fichiers if f.endswith("_valide.json")]
    fichiers_normaux = [f for f in fichiers if f.endswith(".json") and not f.endswith("_valide.json")]

    # Éviter les doublons
    noms_valides = {f.replace("_valide.json", "") for f in fichiers_valides}
    fichiers_sans_doublon = [
        f for f in fichiers_normaux
        if f.replace(".json", "") not in noms_valides
    ]

    tous_les_fichiers = fichiers_valides + fichiers_sans_doublon

    print(f"\nNOVI — Import des cours vers Supabase")
    print(f"Fichiers validés   : {len(fichiers_valides)}")
    print(f"Fichiers normaux   : {len(fichiers_sans_doublon)}")
    print(f"Total à importer   : {len(tous_les_fichiers)}")
    print("="*50)

    cours_importes = []

    for fichier in tous_les_fichiers:
        chemin = os.path.join(dossier, fichier)
        try:
            cours_id = importer_cours(chemin)
            cours_importes.append(cours_id)
            print()
        except Exception as e:
            print(f"Erreur pour {fichier} : {e}\n")

    print("="*50)
    print(f"IMPORT TERMINÉ : {len(cours_importes)} cours importés")
    for c in cours_importes:
        print(f"  ✓ {c}")

if __name__ == "__main__":
    importer_tous_les_cours()