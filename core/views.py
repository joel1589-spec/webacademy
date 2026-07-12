from django.shortcuts import render

from annonces.models import Annonce
from blog.models import Article
from services.models import Service


def accueil(request):
    """Page d'accueil générale du site Web Academy."""
    contexte = {
        'annonces': Annonce.objects.all()[:3],
        'articles': Article.objects.filter(publie=True)[:3],
        'services': Service.objects.filter(actif=True)[:4],
    }
    return render(request, 'core/accueil.html', contexte)
