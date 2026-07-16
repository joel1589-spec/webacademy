"""Correction automatique d'une copie, une fois soumise (ou le temps écoulé)."""

import unicodedata

from django.conf import settings
from django.utils import timezone

from .models import Question


def _normaliser(texte):
    """Compare le texte insensible aux majuscules, accents, et espaces superflus."""
    texte = (texte or "").strip().lower()
    texte = unicodedata.normalize('NFKD', texte)
    texte = ''.join(c for c in texte if not unicodedata.combining(c))
    return ' '.join(texte.split())


SYSTEM_PROMPT_CORRECTION = (
    "Tu es un correcteur pédagogique rigoureux mais bienveillant. On te donne une "
    "question de cours, une ou plusieurs réponses de référence considérées comme "
    "correctes, et la réponse rédigée par un apprenant. Ta seule tâche : dire si la "
    "réponse de l'apprenant est correcte SUR LE FOND, même si elle est formulée "
    "différemment (synonymes, ordre différent, plus ou moins détaillée), tant "
    "qu'elle contient l'idée essentielle attendue et ne contient pas d'erreur ou de "
    "contresens. Réponds uniquement par le mot CORRECT ou le mot INCORRECT, sans "
    "aucun autre mot, sans ponctuation, sans explication."
)


def _ia_juge_correct(question, texte_etudiant, reponses_reference):
    """
    Demande à l'IA si `texte_etudiant` correspond sur le fond à l'une des
    `reponses_reference` pour la `question` donnée.
    Retourne True/False, ou None si l'IA n'a pas pu trancher (clé absente,
    panne, timeout...) — à charge de l'appelant de choisir un repli sûr.
    """
    from assistant.services import _client  # évite un import circulaire au chargement des apps

    references = "\n".join(f"- {texte}" for texte in reponses_reference)
    message_utilisateur = (
        f"Question posée à l'apprenant :\n{question.enonce}\n\n"
        f"Réponse(s) de référence acceptée(s) :\n{references}\n\n"
        f"Réponse rédigée par l'apprenant :\n{texte_etudiant}\n\n"
        "La réponse de l'apprenant est-elle correcte ?"
    )

    try:
        reponse = _client().chat.completions.create(
            model=settings.RODIUMAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_CORRECTION},
                {"role": "user", "content": message_utilisateur},
            ],
            max_tokens=5,
            temperature=0,
            timeout=15,
        )
    except Exception:
        # Panne, quota dépassé, clé absente, timeout... : on ne fait jamais
        # planter la correction à cause d'un souci côté IA.
        return None

    verdict = (reponse.choices[0].message.content or "").strip().upper()
    if verdict.startswith("INCORRECT"):
        return False
    if verdict.startswith("CORRECT"):
        return True
    return None  # réponse inattendue de l'IA : on ne devine pas


def corriger_reponse(reponse):
    """Calcule et enregistre les points obtenus pour une ReponseEtudiant donnée."""
    question = reponse.question

    if question.type_question in (Question.QCM, Question.VRAI_FAUX):
        choix_correctes = set(question.choix_possibles.filter(est_correct=True).values_list('id', flat=True))
        choix_donnees = set(reponse.choix_selectionnes.values_list('id', flat=True))
        points = question.points if (choix_donnees == choix_correctes and choix_donnees) else 0

    elif question.type_question == Question.REPONSE_COURTE:
        texte_etudiant = (reponse.texte_libre or "").strip()
        reponses_acceptees = list(question.reponses_acceptees.values_list('texte', flat=True))

        if not texte_etudiant or not reponses_acceptees:
            # Rien d'écrit, ou aucune réponse de référence définie par le
            # formateur : impossible de juger, on ne prend pas le risque de
            # demander à l'IA de deviner un corrigé qui n'existe pas.
            points = 0
        elif _normaliser(texte_etudiant) in {_normaliser(r) for r in reponses_acceptees}:
            # Correspondance exacte (aux accents/majuscules/espaces près) :
            # pas besoin d'appeler l'IA, c'est instantané et ça ne coûte rien.
            points = question.points
        else:
            verdict = _ia_juge_correct(question, texte_etudiant, reponses_acceptees)
            points = question.points if verdict else 0

    else:
        points = 0

    reponse.points_obtenus = points
    reponse.save(update_fields=['points_obtenus'])
    return points


def corriger_copie(copie):
    """
    Corrige toutes les questions du sujet pour cette copie (celles sans réponse
    comptent pour 0 point), calcule la note finale, et marque la copie comme terminée.
    Peut être appelée aussi bien lors d'une soumission normale que lors d'une
    soumission automatique déclenchée par l'expiration du temps imparti.
    """
    total = 0
    for question in copie.sujet.questions.all():
        reponse = copie.reponses.filter(question=question).first()
        if reponse:
            total += corriger_reponse(reponse)
        # Question sans réponse du tout : 0 point, rien à faire de plus.

    copie.note_obtenue = total
    copie.terminee = True
    copie.date_soumission = timezone.now()
    copie.save(update_fields=['note_obtenue', 'terminee', 'date_soumission'])
    return copie
