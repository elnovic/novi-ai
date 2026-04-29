import os
import time
from groq import Groq
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

nvidia_client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

# Modèles
GROQ_MODEL   = "llama-3.3-70b-versatile"
NVIDIA_MODEL = "meta/llama-3.3-70b-instruct"

def appeler_ia(messages: list, max_tokens: int = 4000, temperature: float = 0.7) -> str:
    """
    Appelle Groq en priorité.
    Si Groq est indisponible ou a atteint sa limite,
    bascule automatiquement sur NVIDIA NIM.
    """

    # ── TENTATIVE 1 : Groq ──
    for tentative in range(2):
        try:
            print("  [IA] Groq...", end=" ")
            reponse = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            print("OK")
            return reponse.choices[0].message.content

        except Exception as e:
            erreur = str(e)
            if "rate_limit_exceeded" in erreur or "429" in erreur:
                if tentative == 0:
                    print(f"Limite atteinte — bascule sur NVIDIA...")
                    break  # Passe directement à NVIDIA
                else:
                    print(f"Groq toujours indisponible.")
            elif "503" in erreur or "unavailable" in erreur.lower():
                print(f"Groq hors ligne — bascule sur NVIDIA...")
                break
            else:
                print(f"Erreur Groq : {e}")
                break

    # ── TENTATIVE 2 : NVIDIA NIM ──
    for tentative in range(3):
        try:
            print("  [IA] NVIDIA NIM...", end=" ")
            reponse = nvidia_client.chat.completions.create(
                model=NVIDIA_MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            print("OK")
            return reponse.choices[0].message.content

        except Exception as e:
            erreur = str(e)
            if "rate_limit" in erreur or "429" in erreur:
                print(f"NVIDIA limite atteinte — attente 60s... (tentative {tentative+1}/3)")
                time.sleep(60)
            else:
                print(f"Erreur NVIDIA : {e}")
                if tentative < 2:
                    print(f"Réessai dans 30s...")
                    time.sleep(30)

    raise Exception("Groq et NVIDIA sont tous les deux indisponibles. Réessaie plus tard.")