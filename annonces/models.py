from django.db import models


class Annonce(models.Model):
    """Une annonce publiée par Web Academy (nouvelle session, événement, information...)."""

    titre = models.CharField("Titre", max_length=200)
    contenu = models.TextField("Contenu")
    image = models.ImageField("Image (optionnelle)", upload_to='annonces/', blank=True, null=True)
    epinglee = models.BooleanField(
        "Épinglée en haut de la liste", default=False,
        help_text="Cocher pour faire apparaître cette annonce en premier.",
    )
    date_publication = models.DateTimeField("Publiée le", auto_now_add=True)

    class Meta:
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"
        ordering = ['-epinglee', '-date_publication']

    def __str__(self):
        return self.titre
