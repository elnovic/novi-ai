from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from novi_ai.generator.generator import generer_cours_complet
from novi_ai.manager.manager import gerer_cours
from novi_ai.recommender.recommender import recommander

app = FastAPI(title="NOVI AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class CoursRequest(BaseModel):
    sujet: str
    niveau: str
    format_cours: str = "théorie + pratique"
    public: str = "étudiants"

class ProfilRequest(BaseModel):
    nom: str
    niveau_actuel: str
    objectifs: list
    domaines_interets: list
    temps_disponible: str = "2 heures par jour"

@app.get("/")
def root():
    return {"status": "NOVI AI Engine opérationnel"}

@app.post("/generer-cours")
def generer_cours(req: CoursRequest):
    cours, chemin = generer_cours_complet(req.sujet, req.niveau, req.format_cours, req.public)
    cours_valide = gerer_cours(chemin)
    return cours_valide

@app.post("/recommander")
def recommander_parcours(req: ProfilRequest):
    profil = req.dict()
    profil["age"] = 20
    profil["cours_deja_suivis"] = []
    profil["style_prefere"] = "pratique"
    resultat = recommander(profil)
    return resultat

@app.get("/cours")
def liste_cours():
    dossier = "novi_ai/courses"
    cours_liste = []
    if os.path.exists(dossier):
        for fichier in os.listdir(dossier):
            if fichier.endswith("_valide.json"):
                with open(f"{dossier}/{fichier}", "r", encoding="utf-8") as f:
                    cours = json.load(f)
                    cours_liste.append({
                        "id": fichier.replace("_valide.json", ""),
                        "titre": cours.get("titre"),
                        "niveau": cours.get("niveau"),
                        "duree_estimee": cours.get("duree_estimee"),
                        "score": cours.get("qualite", {}).get("score_final", 0),
                        "certification": cours.get("qualite", {}).get("certification_novi", False)
                    })
    return cours_liste
from fastapi import UploadFile, File, Form
from novi_ai.oral.evaluateur import transcrire_audio, evaluer_reponse
import tempfile
import shutil

@app.post("/examen-oral/question")
async def evaluer_question_orale(
    audio: UploadFile = File(...),
    question: str = Form(...),
    criteres: str = Form(default="clarté,précision,exemples concrets")
):
    # Sauvegarder le fichier audio temporairement
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        shutil.copyfileobj(audio.file, tmp)
        chemin_tmp = tmp.name

    try:
        # Transcrire avec Whisper
        transcription = transcrire_audio(chemin_tmp)

        # Évaluer avec l'IA
        criteres_liste = criteres.split(",")
        evaluation = evaluer_reponse(question, transcription, criteres_liste)

        return {
            "transcription": transcription,
            "evaluation": evaluation
        }
    finally:
        os.unlink(chemin_tmp)