from django.conf import settings
from django.db import models
from django.utils import timezone

from comptes.models import Etudiant


class Conversation(models.Model):
    """
    Un fil de discussion entre un apprenant et le formateur.
    Un seul fil par apprenant (le formateur y répond depuis son espace dédié).
    """

    etudiant = models.OneToOneField(
        Etudiant,
        on_delete=models.CASCADE,
        related_name='conversation',
        verbose_name="Apprenant",
    )
    date_creation = models.DateTimeField("Créée le", auto_now_add=True)
    date_dernier_message = models.DateTimeField("Dernier message le", default=timezone.now)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-date_dernier_message']

    def __str__(self):
        return f"Conversation avec {self.etudiant}"


class Message(models.Model):
    """Un message individuel au sein d'une conversation apprenant ↔ formateur."""

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name="Conversation"
    )
    expediteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_envoyes',
        verbose_name="Expéditeur",
    )
    contenu = models.TextField("Message")
    date_envoi = models.DateTimeField("Envoyé le", auto_now_add=True)
    lu = models.BooleanField("Lu par le destinataire", default=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['date_envoi']

    def __str__(self):
        return f"{self.expediteur} — {self.contenu[:40]}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Met à jour l'horodatage du dernier message pour trier les conversations
        # du formateur par activité récente.
        Conversation.objects.filter(pk=self.conversation_id).update(date_dernier_message=self.date_envoi)
