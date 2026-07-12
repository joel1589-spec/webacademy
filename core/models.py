from django.db import models  # noqa: F401

# L'application "core" ne définit pas de modèle : elle gère uniquement la page
# d'accueil générale du site, qui agrège du contenu venant des autres applications
# (annonces, blog, services).
