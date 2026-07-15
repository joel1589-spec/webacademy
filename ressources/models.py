from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models

from attestations.models import Formation


def stockage_fichiers_ressources():
    """
    Choisit le bon stockage pour le champ « fichier » (PDF, Word, ZIP...).

    Cloudinary distingue les images (`MediaCloudinaryStorage`, utilisé par défaut
    via DEFAULT_FILE_STORAGE) des autres fichiers (`RawMediaCloudinaryStorage`).
    Un PDF envoyé via le stockage "image" est rejeté par Cloudinary (erreur
    "Invalid image file"), ce qui provoquait le Server Error 500 à l'ajout d'une
    ressource. On utilise donc explicitement le stockage "raw" pour ce champ.
    """
    if getattr(settings, 'USE_CLOUDINARY', False):
        from cloudinary_storage.storage import RawMediaCloudinaryStorage
        return RawMediaCloudinaryStorage()
    return default_storage


class Ressource(models.Model):
    """Un document, une vidéo ou un lien mis à disposition des apprenants."""

    TYPE_DOCUMENT = 'Document'
    TYPE_VIDEO = 'Video'
    TYPE_LIEN = 'Lien'
    TYPE_CHOICES = [
        (TYPE_DOCUMENT, 'Document (PDF, support de cours...)'),
        (TYPE_VIDEO, 'Vidéo'),
        (TYPE_LIEN, 'Lien externe'),
    ]

    titre = models.CharField("Titre", max_length=200)
    description = models.TextField("Description", blank=True)

    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='ressources',
        verbose_name="Formation concernée",
        null=True,
        blank=True,
        help_text="Laisser vide pour rendre la ressource visible par tous les apprenants inscrits.",
    )

    type_ressource = models.CharField("Type", max_length=20, choices=TYPE_CHOICES, default=TYPE_DOCUMENT)
    fichier = models.FileField(
        "Fichier", upload_to='ressources/fichiers/', blank=True, null=True,
        storage=stockage_fichiers_ressources,
    )
    lien = models.URLField("Lien (vidéo ou site externe)", blank=True)

    date_ajout = models.DateTimeField("Ajoutée le", auto_now_add=True)
    ordre = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"
        ordering = ['ordre', '-date_ajout']

    def __str__(self):
        return self.titre

    @property
    def url_acces(self):
        if self.fichier:
            return self.fichier.url
        return self.lien
