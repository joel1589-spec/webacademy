from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Article(models.Model):
    """Un article de blog publié par Web Academy (conseils, actualités, retours d'expérience)."""

    titre = models.CharField("Titre", max_length=200)
    slug = models.SlugField("Slug (URL)", max_length=220, unique=True, blank=True)
    resume = models.CharField("Résumé (affiché dans la liste)", max_length=300)
    contenu = models.TextField("Contenu de l'article")
    image = models.ImageField("Image de couverture", upload_to='blog/', blank=True, null=True)
    categorie = models.CharField("Catégorie", max_length=100, blank=True, help_text="Ex : Conseils, Actualités, Témoignages")

    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles',
        verbose_name="Auteur",
    )

    publie = models.BooleanField("Publié", default=True)
    date_publication = models.DateTimeField("Publié le", auto_now_add=True)

    class Meta:
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titre)[:200]
            slug = base_slug
            i = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base_slug}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)
