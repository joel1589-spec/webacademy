#!/usr/bin/env python
"""Utilitaire en ligne de commande de Django pour le projet Web Academy - Vérification des attestations."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webacademy_verif.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Avez-vous bien activé votre environnement "
            "virtuel et installé les dépendances (pip install -r requirements.txt) ?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
