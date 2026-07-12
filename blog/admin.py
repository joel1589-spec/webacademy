from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'auteur', 'publie', 'date_publication')
    list_editable = ('publie',)
    search_fields = ('titre', 'resume', 'contenu')
    list_filter = ('publie', 'categorie')
    prepopulated_fields = {'slug': ('titre',)}
