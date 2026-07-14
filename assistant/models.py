from django.db import models
from django.utils import timezone

from comptes.models import Etudiant


class Conversation(models.Model):
    """Un fil de discussion entre un apprenant et l'assistant IA (un seul fil par apprenant)."""

    etudiant = models.OneToOneField(
        Etudiant,
        on_delete=models.CASCADE,
        related_name='conversation_ia',
        verbose_name="Apprenant",
    )
    date_creation = models.DateTimeField("Créée le", auto_now_add=True)
    date_dernier_message = models.DateTimeField("Dernier message le", default=timezone.now)

    class Meta:
        verbose_name = "Conversation avec l'assistant IA"
        verbose_name_plural = "Conversations avec l'assistant IA"
        ordering = ['-date_dernier_message']

    def __str__(self):
        return f"Assistant IA — {self.etudiant}"


class Message(models.Model):
    """Un message individuel (question de l'apprenant ou réponse de l'IA)."""

    ROLE_ETUDIANT = 'etudiant'
    ROLE_IA = 'ia'
    CHOIX_ROLE = [
        (ROLE_ETUDIANT, "Apprenant"),
        (ROLE_IA, "Assistant IA"),
    ]

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name="Conversation"
    )
    role = models.CharField("Auteur", max_length=10, choices=CHOIX_ROLE)
    contenu = models.TextField("Message")
    date_envoi = models.DateTimeField("Envoyé le", auto_now_add=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['date_envoi']

    def __str__(self):
        return f"{self.get_role_display()} — {self.contenu[:40]}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Conversation.objects.filter(pk=self.conversation_id).update(date_dernier_message=self.date_envoi)
