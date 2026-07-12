import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Crée (une seule fois) le compte formateur/administrateur à partir de
    variables d'environnement, plutôt que d'écrire des identifiants en dur
    dans le code. Prévu pour être exécuté à chaque déploiement (build.sh) :
    si le compte existe déjà ou si les variables ne sont pas définies, la
    commande ne fait rien — elle peut donc être relancée sans risque.

    Variables d'environnement attendues (à définir sur Render, jamais dans Git) :
      - DJANGO_SUPERUSER_USERNAME
      - DJANGO_SUPERUSER_EMAIL
      - DJANGO_SUPERUSER_PASSWORD
    """

    help = "Crée le compte administrateur à partir de variables d'environnement (idempotent)."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(
                "creer_admin : DJANGO_SUPERUSER_USERNAME/PASSWORD non définis, "
                "aucune action (rien à créer)."
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                f"creer_admin : le compte « {username} » existe déjà, aucune action."
            )
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(
            f"creer_admin : compte administrateur « {username} » créé avec succès."
        ))
