from django.conf import settings
from django.db import models

from attestations.models import Formation


class Etudiant(models.Model):
    """Profil apprenant lié à un compte utilisateur Django (connexion classique)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='etudiant',
        verbose_name="Utilisateur",
    )

    telephone = models.CharField("Téléphone", max_length=30, blank=True)
    ville = models.CharField("Ville", max_length=100, blank=True)
    photo = models.ImageField(
        "Photo de profil", upload_to='profils/', blank=True, null=True
    )
    bio = models.TextField("À propos de moi", blank=True)

    formations_suivies = models.ManyToManyField(
        Formation,
        blank=True,
        related_name='etudiants',
        verbose_name="Formations suivies",
        help_text="Formations auxquelles cet apprenant est inscrit (donne accès aux ressources associées).",
    )

    attestations = models.ManyToManyField(
        'attestations.Attestation',
        blank=True,
        related_name='apprenants',
        verbose_name="Attestations liées",
        help_text=(
            "Attestations rattachées à ce compte apprenant (liaison automatique par "
            "correspondance de nom, ou ajoutées manuellement par l'apprenant via son numéro)."
        ),
    )

    date_inscription = models.DateTimeField("Inscrit le", auto_now_add=True)

    class Meta:
        verbose_name = "Apprenant"
        verbose_name_plural = "Apprenants"
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
