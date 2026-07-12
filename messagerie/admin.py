from django.contrib import admin

from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('expediteur', 'contenu', 'date_envoi', 'lu')
    can_delete = False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'date_creation', 'date_dernier_message')
    search_fields = ('etudiant__user__first_name', 'etudiant__user__last_name')
    inlines = [MessageInline]
