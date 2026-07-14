from django.contrib import admin

from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ('role', 'contenu', 'date_envoi')
    readonly_fields = ('role', 'contenu', 'date_envoi')
    can_delete = False
    ordering = ['date_envoi']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Lecture seule volontairement : ces échanges servent à surveiller le bon
    usage de l'assistant IA (éviter les abus, repérer des questions
    problématiques), pas à être modifiés depuis l'admin.
    """
    list_display = ('etudiant', 'date_creation', 'date_dernier_message', 'nombre_messages')
    search_fields = ('etudiant__user__first_name', 'etudiant__user__last_name', 'etudiant__user__email')
    ordering = ('-date_dernier_message',)
    inlines = [MessageInline]
    readonly_fields = ('etudiant', 'date_creation', 'date_dernier_message')

    @admin.display(description="Messages")
    def nombre_messages(self, obj):
        return obj.messages.count()

    def has_add_permission(self, request):
        return False
