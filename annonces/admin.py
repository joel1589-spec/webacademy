from django.contrib import admin

from .models import Annonce


@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'epinglee', 'date_publication')
    list_editable = ('epinglee',)
    search_fields = ('titre', 'contenu')
    list_filter = ('epinglee',)
