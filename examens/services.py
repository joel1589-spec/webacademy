"""Correction automatique d'une copie, une fois soumise (ou le temps écoulé)."""

import unicodedata

from django.utils import timezone

from .models import Question


def _normaliser(texte):
    """Compare le texte insensible aux majuscules, accents, et espaces superflus."""
    texte = (texte or "").strip().lower()
    texte = unicodedata.normalize('NFKD', texte)
    texte = ''.join(c for c in texte if not unicodedata.combining(c))
    return ' '.join(texte.split())


def corriger_reponse(reponse):
    """Calcule et enregistre les points obtenus pour une ReponseEtudiant donnée."""
    question = reponse.question

    if question.type_question in (Question.QCM, Question.VRAI_FAUX):
        choix_correctes = set(question.choix_possibles.filter(est_correct=True).values_list('id', flat=True))
        choix_donnees = set(reponse.choix_selectionnes.values_list('id', flat=True))
        points = question.points if (choix_donnees == choix_correctes and choix_donnees) else 0

    elif question.type_question == Question.REPONSE_COURTE:
        reponses_valides = {_normaliser(r) for r in question.reponses_acceptees.values_list('texte', flat=True)}
        points = question.points if _normaliser(reponse.texte_libre) in reponses_valides else 0

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
