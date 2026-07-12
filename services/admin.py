from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'icone', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('titre', 'description')
