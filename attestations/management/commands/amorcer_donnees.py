from django.core.management.base import BaseCommand

from attestations.models import Formation


class Command(BaseCommand):
    help = "Crée une formation de démarrage pour pouvoir tester le site immédiatement."

    def handle(self, *args, **options):
        formation, cree = Formation.objects.get_or_create(
            nom="Développement Web (HTML, CSS, JavaScript)"
        )
        if cree:
            self.stdout.write(self.style.SUCCESS(f"Formation créée : {formation.nom}"))
        else:
            self.stdout.write(f"Formation déjà existante : {formation.nom}")
