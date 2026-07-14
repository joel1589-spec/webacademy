"""
Intégration avec RodiumAI (https://rodiumai.io) : une passerelle qui expose
plusieurs modèles d'IA (Claude, GPT, Gemini...) via une seule clé et une API
compatible OpenAI. On utilise donc simplement la librairie `openai` officielle,
pointée vers le serveur de RodiumAI au lieu de celui d'OpenAI.
"""

from django.conf import settings
from openai import OpenAI, APIError, APITimeoutError

SYSTEM_PROMPT = (
    "Tu es l'assistant pédagogique de Web Academy, une école de formation aux "
    "métiers du numérique (développement web, cybersécurité, bureautique et "
    "outils digitaux) basée au Togo. Tu réponds aux questions des apprenants "
    "de façon claire, bienveillante et pédagogique, en français par défaut "
    "(sauf si l'apprenant écrit dans une autre langue). Tu peux répondre à "
    "toutes sortes de questions, pas uniquement sur les cours. Reste concis "
    "et concret, avec des exemples quand c'est utile."
)

# Nombre de messages précédents (question + réponse) renvoyés comme contexte
# à chaque nouvelle question, pour garder une conversation cohérente sans
# faire exploser le coût de chaque appel.
NB_MESSAGES_CONTEXTE = 12


class ErreurAssistantIA(Exception):
    """Levée quand l'appel à l'IA échoue, pour affichage d'un message clair à l'apprenant."""


def _client():
    if not settings.RODIUMAI_API_KEY:
        raise ErreurAssistantIA(
            "La clé API de l'assistant IA n'est pas configurée (variable RODIUMAI_API_KEY)."
        )
    return OpenAI(api_key=settings.RODIUMAI_API_KEY, base_url=settings.RODIUMAI_BASE_URL)


def demander_a_l_ia(messages_precedents, nouvelle_question):
    """
    messages_precedents : liste d'objets Message (ordre chronologique), déjà en base.
    nouvelle_question : texte de la question posée par l'apprenant (pas encore en base).
    Retourne le texte de la réponse de l'IA, ou lève ErreurAssistantIA.
    """
    historique = []
    for message in messages_precedents[-NB_MESSAGES_CONTEXTE:]:
        role_openai = 'assistant' if message.role == 'ia' else 'user'
        historique.append({"role": role_openai, "content": message.contenu})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + historique + [
        {"role": "user", "content": nouvelle_question}
    ]

    try:
        reponse = _client().chat.completions.create(
            model=settings.RODIUMAI_MODEL,
            messages=messages,
            max_tokens=800,
            timeout=30,
        )
    except APITimeoutError:
        raise ErreurAssistantIA("L'assistant IA met trop de temps à répondre. Réessaie dans un instant.")
    except APIError as exc:
        raise ErreurAssistantIA(f"L'assistant IA n'a pas pu répondre pour le moment ({exc}).")
    except Exception as exc:  # sécurité : jamais de 500 côté apprenant à cause de l'IA
        raise ErreurAssistantIA(f"L'assistant IA n'a pas pu répondre pour le moment ({exc}).")

    contenu = reponse.choices[0].message.content
    return (contenu or "").strip() or "Désolé, je n'ai pas pu formuler de réponse cette fois-ci."
