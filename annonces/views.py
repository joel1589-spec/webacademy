from django.shortcuts import get_object_or_404, render

from .models import Annonce


def liste(request):
    """Liste publique des annonces de Web Academy."""
    annonces = Annonce.objects.all()
    return render(request, 'annonces/liste.html', {'annonces': annonces})


def detail(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    return render(request, 'annonces/detail.html', {'annonce': annonce})
