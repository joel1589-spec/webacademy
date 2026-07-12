from django.shortcuts import get_object_or_404, render

from .models import Article


def liste(request):
    """Liste publique des articles de blog publiés."""
    articles = Article.objects.filter(publie=True)
    return render(request, 'blog/liste.html', {'articles': articles})


def detail(request, slug):
    article = get_object_or_404(Article, slug=slug, publie=True)
    return render(request, 'blog/detail.html', {'article': article})
