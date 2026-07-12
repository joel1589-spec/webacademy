from django.shortcuts import render

from .models import Service


def liste(request):
    """Page publique de présentation des services de Web Academy."""
    services = Service.objects.filter(actif=True)
    return render(request, 'services/liste.html', {'services': services})
