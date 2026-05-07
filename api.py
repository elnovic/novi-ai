from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client
import json
import os
import time
from dotenv import load_dotenv
from novi_ai.models.ai_client import appeler_ia
from novi_ai.manager.manager import gerer_cours

load_dotenv()

app = FastAPI(title="NOVI AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# Client Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

class CoursRequest(BaseModel):
    sujet: str
    niveau: str
    domaine: str = "IA"
    format_cours: str = "théorie + pratique"
    public: str = "étudiants"

def extraire_json(texte: str) -> dict:
    debut = texte.find("{")
    fin = texte.rfind("}") + 1
    if debut == -1 or fin == 0:
        raise ValueError("JSON non trouvé")
    return json.loads(texte[debut:fin])

def nettoyer_id(texte: str) -> str:
    nom = texte.lower()
    remplacements = {
        " ": "_", "'": "", "é": "e", "è": "e", "ê": "e",
        "à": "a", "ô": "o", "î": "i", "ù": "u", "ç": "c",
        ",": "", ":": "", "!": "", "?": "", "&": "et", "/": "_"
    }
    for ancien, nouveau in remplacements.items():
        nom = nom.replace(ancien, nouveau)
    return nom[:50]

@app.get("/")
def root():
    return {"status": "NOVI AI Engine opérationnel", "version": "2.0"}

@app.get("/cours")
def liste_cours():
    result = supabase.table("cours").select(
        "id, titre, niveau, domaine, duree_estimee, score_qualite, certification, created_at"
    ).order("created_at", desc=True).execute()
    return result.data or []

@app.post("/generer-cours")
def generer_cours_complet(req: CoursRequest):
    print(f"\nGénération : {req.sujet}")
    os.makedirs("novi_ai/courses", exist_ok=True)
    nom_fichier = nettoyer_id(req.sujet)
    chemin = f"novi_ai/courses/{nom_fichier}.json"

    # Générer le plan
    plan_brut = appeler_ia([
        {"role": "system", "content": "Tu es un expert pédagogue pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."},
        {"role": "user", "content": f"""Crée le plan d'un cours sur "{req.sujet}" niveau {req.niveau} pour {req.public}.
Réponds UNIQUEMENT en JSON :
{{
  "titre": "...",
  "description": "description engageante de 3-4 phrases",
  "niveau": "{req.niveau}",
  "duree_estimee": "...",
  "objectifs": ["obj1", "obj2", "obj3", "obj4", "obj5"],
  "chapitres_prevus": [
    {{"numero": 1, "titre": "..."}},
    {{"numero": 2, "titre": "..."}},
    {{"numero": 3, "titre": "..."}},
    {{"numero": 4, "titre": "..."}},
    {{"numero": 5, "titre": "..."}}
  ]
}}"""}
    ], max_tokens=1000)
    plan = extraire_json(plan_brut)

    # Générer les chapitres
    chapitres = []
    for ch in plan['chapitres_prevus']:
        print(f"  Chapitre {ch['numero']}...")
        ch_brut = appeler_ia([
            {"role": "system", "content": "Tu es un expert pédagogue pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."},
            {"role": "user", "content": f"""Génère le chapitre {ch['numero']} : "{ch['titre']}" niveau {req.niveau}.
Réponds UNIQUEMENT en JSON :
{{
  "numero": {ch['numero']},
  "titre": "{ch['titre']}",
  "contenu": "explication détaillée minimum 10 phrases",
  "points_cles": ["point 1", "point 2", "point 3", "point 4"],
  "exemple_concret": "exemple réel et précis",
  "anecdote": "anecdote intéressante",
  "quiz": [
    {{"question": "question ?", "options": ["A", "B", "C", "D"], "bonne_reponse": "A", "explication": "explication"}},
    {{"question": "question 2 ?", "options": ["A", "B", "C", "D"], "bonne_reponse": "B", "explication": "explication"}}
  ],
  "exercice": {{
    "type": "pratique",
    "enonce": "description de l'exercice",
    "instructions": ["étape 1", "étape 2", "étape 3", "étape 4"],
    "livrable": "ce que l'apprenant rend",
    "conseil": "conseil pour réussir"
  }}
}}"""}
        ], max_tokens=4000)
        try:
            chapitres.append(extraire_json(ch_brut))
        except Exception as e:
            print(f"  Erreur chapitre {ch['numero']} : {e}")
        time.sleep(1)

    # Générer projet final + examen
    final_brut = appeler_ia([
        {"role": "system", "content": "Tu es un expert pédagogue pour NOVI Académie. Tu réponds UNIQUEMENT en JSON valide."},
        {"role": "user", "content": f"""Pour le cours "{plan['titre']}", génère le projet final et l'examen oral.
Réponds UNIQUEMENT en JSON :
{{
  "projet_final": {{
    "titre": "...", "description": "...",
    "etapes": ["1", "2", "3", "4", "5"],
    "criteres_evaluation": ["1", "2", "3"],
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
}}"""}
    ], max_tokens=2000)
    final = extraire_json(final_brut)

    cours = {
        "titre": plan["titre"],
        "description": plan["description"],
        "niveau": plan["niveau"],
        "domaine": req.domaine,
        "duree_estimee": plan["duree_estimee"],
        "objectifs": plan["objectifs"],
        "chapitres": chapitres,
        "projet_final": final["projet_final"],
        "examen_oral": final["examen_oral"],
        "ressources": final["ressources"]
    }

    # Sauvegarder localement
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(cours, f, ensure_ascii=False, indent=2)

    # Valider avec le Course Manager
    print("Course Manager...")
    cours_valide = gerer_cours(chemin)

    # Importer dans Supabase automatiquement
    cours_id = nettoyer_id(cours_valide["titre"])
    supabase.table("cours").upsert({
        "id": cours_id,
        "titre": cours_valide["titre"],
        "description": cours_valide.get("description", ""),
        "niveau": cours_valide.get("niveau", req.niveau),
        "domaine": req.domaine,
        "duree_estimee": cours_valide.get("duree_estimee", "10 heures"),
        "score_qualite": cours_valide.get("qualite", {}).get("score_final", 85),
        "certification": cours_valide.get("qualite", {}).get("certification_novi", True),
        "contenu": cours_valide
    }).execute()

    print(f"Cours importé dans Supabase : {cours_id}")
    return cours_valide

@app.delete("/cours/{cours_id}")
def supprimer_cours(cours_id: str):
    supabase.table("cours").delete().eq("id", cours_id).execute()
    return {"message": f"Cours {cours_id} supprimé"}

@app.put("/cours/{cours_id}/certification")
def toggle_certification(cours_id: str, actif: bool):
    supabase.table("cours").update({"certification": actif}).eq("id", cours_id).execute()
    return {"message": f"Certification mise à jour"}

@app.get("/stats")
def get_stats():
    cours = supabase.table("cours").select("id", count="exact").execute()
    users = supabase.table("utilisateurs").select("id", count="exact").execute()
    pubs = supabase.table("publications").select("id", count="exact").execute()
    ops = supabase.table("opportunites").select("id", count="exact").execute()
    admins = supabase.table("utilisateurs").select("id", count="exact").eq("role", "admin").execute()
    derniers = supabase.table("utilisateurs").select("prenom, nom, email, niveau, created_at").order("created_at", desc=True).limit(8).execute()

    return {
        "cours": cours.count or 0,
        "utilisateurs": users.count or 0,
        "publications": pubs.count or 0,
        "opportunites": ops.count or 0,
        "admins": admins.count or 0,
        "derniers_inscrits": derniers.data or []
    }

@app.get("/publications")
def get_publications():
    result = supabase.table("publications").select("*").order("created_at", desc=True).execute()
    return result.data or []

@app.put("/publications/{pub_id}/statut")
def update_publication_statut(pub_id: str, statut: str):
    supabase.table("publications").update({"statut": statut}).eq("id", pub_id).execute()
    return {"message": "Statut mis à jour"}

@app.get("/opportunites")
def get_opportunites():
    result = supabase.table("opportunites").select("*").order("created_at", desc=True).execute()
    return result.data or []

@app.post("/opportunites")
def creer_opportunite(data: dict):
    supabase.table("opportunites").insert(data).execute()
    return {"message": "Opportunité créée"}

@app.delete("/opportunites/{op_id}")
def supprimer_opportunite(op_id: str):
    supabase.table("opportunites").delete().eq("id", op_id).execute()
    return {"message": "Opportunité supprimée"}

@app.get("/utilisateurs")
def get_utilisateurs():
    result = supabase.table("utilisateurs").select("*").order("created_at", desc=True).execute()
    return result.data or []

@app.put("/utilisateurs/{user_id}/role")
def update_role(user_id: str, role: str):
    supabase.table("utilisateurs").update({"role": role}).eq("id", user_id).execute()
    return {"message": f"Rôle mis à jour : {role}"}