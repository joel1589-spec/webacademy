from django.contrib import admin

from .models import Ressource


@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'formation', 'type_ressource', 'date_ajout', 'ordre')
    list_filter = ('type_ressource', 'formation')
    search_fields = ('titre', 'description')
    ordering = ('ordre', '-date_ajout')
