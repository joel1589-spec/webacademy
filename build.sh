#!/usr/bin/env bash
# Script exécuté par Render à chaque déploiement.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input --upload-unhashed-files
python manage.py migrate
python manage.py creer_admin
