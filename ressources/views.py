from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from comptes.models import Etudiant

from .models import Ressource


@login_required(login_url='comptes:connexion')
def liste(request):
    """
    Liste des ressources pédagogiques réservée aux apprenants connectés
    (section 'espace personnel apprenant' — ressources disponibles).
    Le personnel (staff) voit toutes les ressources ; un apprenant ne voit que
    celles de ses formations, plus celles communes à tous.
    """
    if request.user.is_staff:
        ressources = Ressource.objects.select_related('formation').all()
    else:
        etudiant, _ = Etudiant.objects.get_or_create(user=request.user)
        formations = etudiant.formations_suivies.all()
        ressources = (
            Ressource.objects.filter(formation__in=formations)
            | Ressource.objects.filter(formation__isnull=True)
        ).distinct().select_related('formation')

    contexte = {'ressources': ressources}
    return render(request, 'ressources/liste.html', contexte)
