from django.db import models


class Service(models.Model):
    """Un service proposé par Web Academy, présenté sur la page publique 'Services'."""

    titre = models.CharField("Titre", max_length=150)
    description = models.TextField("Description")
    icone = models.CharField(
        "Icône (emoji)", max_length=10, default="🎓",
        help_text="Un emoji simple à afficher devant le titre, ex : 🎓 💻 🧑‍🏫",
    )
    ordre = models.PositiveIntegerField("Ordre d'affichage", default=0)
    actif = models.BooleanField("Visible sur le site", default=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['ordre', 'titre']

    def __str__(self):
        return self.titre
