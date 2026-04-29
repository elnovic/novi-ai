from novi_ai.models.ai_client import appeler_ia

print("Test du système de fallback NOVI...\n")

reponse = appeler_ia([
    {
        "role": "system",
        "content": "Tu es un assistant NOVI. Tu réponds en une phrase courte."
    },
    {
        "role": "user",
        "content": "Dis bonjour à NOVI Ecosystem en une phrase."
    }
], max_tokens=100)

print(f"\nRéponse : {reponse}")
print("\nSystème de fallback opérationnel !")