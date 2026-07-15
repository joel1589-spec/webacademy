from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from comptes.models import Etudiant

from .models import Choix, Copie, Question, ReponseEtudiant, Sujet
from .services import corriger_copie


@login_required(login_url='comptes:connexion')
def liste_sujets(request):
    """Liste des sujets disponibles pour l'apprenant, avec son statut sur chacun."""
    etudiant, _ = Etudiant.objects.get_or_create(user=request.user)
    sujets = Sujet.objects.filter(actif=True)
    copies_par_sujet = {c.sujet_id: c for c in Copie.objects.filter(etudiant=etudiant)}

    lignes = []
    for sujet in sujets:
        lignes.append({'sujet': sujet, 'copie': copies_par_sujet.get(sujet.id)})

    return render(request, 'examens/liste_sujets.html', {'lignes': lignes})


def _temps_restant_secondes(copie):
    fin = copie.date_debut + timezone.timedelta(minutes=copie.sujet.duree_minutes)
    return (fin - timezone.now()).total_seconds()


@login_required(login_url='comptes:connexion')
def traiter_sujet(request, sujet_id):
    """Affiche le sujet à traiter, avec minuteur, et reçoit la soumission des réponses."""
    etudiant, _ = Etudiant.objects.get_or_create(user=request.user)
    sujet = get_object_or_404(Sujet, pk=sujet_id, actif=True)

    copie, _ = Copie.objects.get_or_create(sujet=sujet, etudiant=etudiant)

    if copie.terminee:
        return redirect('examens:resultat_copie', copie_id=copie.id)

    temps_restant = _temps_restant_secondes(copie)
    temps_ecoule = temps_restant <= 0

    if request.method == 'POST' or temps_ecoule:
        # Soumission normale (bouton cliqué à temps) ou soumission automatique
        # (temps écoulé) : on enregistre ce qui est rempli, puis on corrige.
        for question in sujet.questions.all():
            reponse, _ = ReponseEtudiant.objects.get_or_create(copie=copie, question=question)
            if question.type_question == Question.REPONSE_COURTE:
                reponse.texte_libre = request.POST.get(f'question_{question.id}', '')
                reponse.save(update_fields=['texte_libre'])
            else:
                ids_choisis = request.POST.getlist(f'question_{question.id}')
                reponse.choix_selectionnes.set(Choix.objects.filter(id__in=ids_choisis, question=question))

        corriger_copie(copie)
        if temps_ecoule and request.method != 'POST':
            django_messages.info(request, "Le temps imparti est écoulé : ta copie a été soumise automatiquement.")
        return redirect('examens:resultat_copie', copie_id=copie.id)

    contexte = {
        'sujet': sujet,
        'copie': copie,
        'questions': sujet.questions.all(),
        'temps_restant_secondes': int(temps_restant),
    }
    return render(request, 'examens/traiter_sujet.html', contexte)


@login_required(login_url='comptes:connexion')
def resultat_copie(request, copie_id):
    etudiant, _ = Etudiant.objects.get_or_create(user=request.user)
    copie = get_object_or_404(Copie, pk=copie_id, etudiant=etudiant)

    if not copie.terminee:
        return redirect('examens:traiter_sujet', sujet_id=copie.sujet_id)

    details = []
    for question in copie.sujet.questions.all():
        reponse = copie.reponses.filter(question=question).first()
        details.append({
            'question': question,
            'reponse': reponse,
            'correcte': bool(reponse and reponse.points_obtenus == question.points),
        })

    return render(request, 'examens/resultat_copie.html', {'copie': copie, 'details': details})
