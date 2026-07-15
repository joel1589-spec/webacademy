"""
Configuration Django — Site de vérification des attestations Web Academy.

⚠️ Avant la mise en production :
  - changer SECRET_KEY (utiliser une variable d'environnement)
  - passer DEBUG = False
  - renseigner ALLOWED_HOSTS avec votre vrai nom de domaine
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Sécurité ---------------------------------------------------------------

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'dev-secret-key-a-changer-absolument-avant-mise-en-production'
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

# Render fournit automatiquement le nom d'hôte externe du service dans cette
# variable d'environnement (ex : webacademy-verif.onrender.com) — on l'ajoute
# aux hôtes autorisés sans que tu aies besoin de la recopier à la main.
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_EXTERNAL_HOSTNAME}"]

# URL publique du site (sans slash final), utilisée pour générer des liens
# absolus dans les QR codes des attestations. À définir en production, ex :
# SITE_URL=https://verification.webacademy.tg
SITE_URL = os.environ.get(
    'SITE_URL',
    f"https://{RENDER_EXTERNAL_HOSTNAME}" if RENDER_EXTERNAL_HOSTNAME else 'http://127.0.0.1:8000',
)

# --- Applications -------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'comptes',
    'attestations',
    'ressources',
    'services',
    'annonces',
    'blog',
    'messagerie',
    'assistant',
    'examens',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webacademy_verif.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'messagerie.context_processors.compteur_messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webacademy_verif.wsgi.application'

# --- Base de données ----------------------------------------------------------
# En local (pas de DATABASE_URL) : SQLite, aucune config nécessaire.
# En production : PostgreSQL externe (Neon), via la variable DATABASE_URL.
# conn_max_age=0 : Neon est une base "serverless" qui peut mettre la connexion
# en veille ; on désactive donc la persistance de connexion Django pour éviter
# des erreurs de connexion "périmée" après une période d'inactivité.

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=0,
    )
}

# --- Validation des mots de passe ---------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalisation ------------------------------------------------------

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Lome'
USE_I18N = True
USE_TZ = True

# --- Fichiers statiques ---------------------------------------------------------

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'attestations' / 'static',
    BASE_DIR / 'core' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- Fichiers envoyés par les utilisateurs (photos de profil, documents, images) --

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Assistant IA (RodiumAI) -----------------------------------------------------
# RodiumAI est une passerelle qui donne accès à plusieurs IA (Claude, GPT,
# Gemini...) via une seule clé, avec une API compatible OpenAI. La clé ne doit
# JAMAIS être écrite ici : elle est définie en variable d'environnement
# (RODIUMAI_API_KEY), sur Render dans Environment Variables.
RODIUMAI_API_KEY = os.environ.get('RODIUMAI_API_KEY', '')
RODIUMAI_BASE_URL = os.environ.get('RODIUMAI_BASE_URL', 'https://api.rodiumai.io/v1')
# Identifiant du modèle au format "fournisseur/modèle", ex : anthropic/claude-3-5-sonnet,
# openai/gpt-4o, google/gemini-1.5-pro... Voir https://www.rodiumai.io/models
RODIUMAI_MODEL = os.environ.get('RODIUMAI_MODEL', 'anthropic/claude-3-5-sonnet')
# Nombre maximum de questions qu'un même apprenant peut poser par jour (protection
# contre un usage abusif de la clé API, qui a un coût réel).
ASSISTANT_QUOTA_QUOTIDIEN = int(os.environ.get('ASSISTANT_QUOTA_QUOTIDIEN', '30'))

# --- Connexion / déconnexion ----------------------------------------------------
# Le formateur se connecte via /admin/ (back-office Django) pour gérer les
# attestations, ressources, annonces, articles, services, etc.
# Les apprenants se connectent via /comptes/connexion/ pour accéder à leur
# espace personnel (ressources de formation, profil).

LOGIN_URL = 'comptes:connexion'
LOGIN_REDIRECT_URL = 'comptes:mon_espace'
LOGOUT_REDIRECT_URL = 'core:accueil'
