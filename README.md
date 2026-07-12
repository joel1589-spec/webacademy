# Site complet Web Academy — 100% Django

Ce projet a évolué au-delà du cahier des charges initial (qui ne couvrait que la
vérification des attestations). Il s'agit maintenant du **site complet de Web
Academy** : vitrine, comptes apprenants, ressources de formation, services,
annonces, blog, et bien sûr la vérification d'attestations d'origine.

## 1. Installation

```bash
# 1. Créer et activer un environnement virtuel
python3 -m venv venv
source venv/bin/activate        # sous Windows : venv\Scripts\activate

# 2. Installer les dépendances (Django + Pillow, pour les images/photos)
pip install -r requirements.txt

# 3. Créer la base de données (SQLite, aucune configuration nécessaire)
python manage.py migrate

# 4. Créer votre compte administrateur (formateur)
python manage.py createsuperuser

# 5. (Optionnel) créer du contenu de démonstration :
#    services, annonces, articles de blog, ressources, et un compte
#    apprenant de test (identifiant : demo.etudiant / mot de passe : WebAcademy2026!)
python manage.py amorcer_donnees
python manage.py amorcer_site

# 6. Lancer le serveur de développement
python manage.py runserver
```

Le site est alors accessible sur http://127.0.0.1:8000/

## 2. Plan du site

| URL | Contenu | Accès |
|---|---|---|
| `/` | Page d'accueil générale (vitrine, dernières annonces, blog, services) | Public |
| `/comptes/inscription/` | Créer un compte apprenant | Public |
| `/comptes/connexion/` | Connexion apprenant | Public |
| `/comptes/mon-espace/` | Tableau de bord personnel (profil, formations, ressources) | Apprenant connecté |
| `/comptes/mon-espace/modifier/` | Modifier son profil | Apprenant connecté |
| `/comptes/mon-espace/mes-attestations/` | Attestations reliées à mon compte + formulaire de liaison manuelle | Apprenant connecté |
| `/messagerie/` | Ma conversation avec le formateur (apprenant) / boîte de réception (formateur) | Connecté (contenu différent selon le rôle) |
| `/ressources/` | Documents, vidéos et liens de formation | Apprenant connecté |
| `/services/` | Présentation des services de Web Academy | Public |
| `/annonces/` | Liste et détail des annonces | Public |
| `/blog/` | Liste et détail des articles de blog | Public |
| `/verification/` | Recherche par numéro d'attestation (fonctionnalité d'origine) | Public |
| `/verification/tableau-de-bord/` | Statistiques des attestations délivrées | Formateur (staff) |
| `/admin/` | Back-office complet : gérer apprenants, ressources, services, annonces, articles, attestations | Formateur (staff/superuser) |

Le formateur gère **tout** le contenu (services, annonces, blog, ressources,
apprenants, attestations) depuis `/admin/`, sans avoir besoin d'écrire de code.

## 3. Comptes et rôles

- **Apprenant** : crée son propre compte via `/comptes/inscription/`. Accède à
  son espace personnel et aux ressources de ses formations (le formateur relie
  un apprenant à une ou plusieurs formations depuis `/admin/` → Apprenants).
- **Formateur (administrateur)** : compte créé via `createsuperuser`, se
  connecte sur `/admin/`. Peut tout gérer : ajouter une ressource, publier une
  annonce ou un article de blog, modifier un service, délivrer une attestation,
  associer un apprenant à ses formations.

Les ressources ajoutées sans formation associée sont visibles par **tous**
les apprenants connectés (ressources communes). Une ressource associée à une
formation n'est visible que par les apprenants inscrits à cette formation.

## 4. Structure du projet

```
webacademy_verif/
├── manage.py
├── requirements.txt
├── templates/base.html          # gabarit partagé par tout le site (hors module attestations)
├── webacademy_verif/             # configuration du projet Django
│   ├── settings.py
│   └── urls.py                   # inclut tous les modules ci-dessous
├── core/                          # page d'accueil générale + commande de démo
│   └── management/commands/amorcer_site.py
├── comptes/                        # comptes et espace personnel apprenant
│   ├── models.py                   # Etudiant (profil lié à un User Django)
│   ├── forms.py                    # inscription, modification de profil
│   └── views.py
├── attestations/                    # fonctionnalité d'origine, inchangée
├── ressources/                       # documents/vidéos/liens de formation
├── services/                          # présentation des services proposés
├── annonces/                           # annonces publiques
└── blog/                                # articles de blog
```

## 5. Design

Toutes les nouvelles pages réutilisent la charte graphique navy / or / rouge
déjà définie pour le module de vérification des attestations
(`core/static/core/css/site.css`), afin de garder une identité visuelle
cohérente sur l'ensemble du site.

## 6. Déploiement en production

1. Définir `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS`.
2. Exécuter `python manage.py collectstatic`.
3. Prévoir un espace de stockage persistant pour `MEDIA_ROOT` (photos de
   profil, images des annonces/articles, fichiers de ressources) — un disque
   simple suffit au démarrage, un stockage objet (S3, etc.) sera utile si le
   site grossit beaucoup.
4. Déployer sur un hébergeur Python (Render, Railway, PythonAnywhere, VPS +
   Gunicorn/Nginx). Activer HTTPS.

## 7. Fonctionnalités ajoutées récemment

- **Messagerie interne** (`/messagerie/`) : chaque apprenant a une conversation
  privée avec le formateur (`Mon espace → 💬 Messagerie`). Le formateur consulte
  toutes les conversations sur `/messagerie/` (liste avec badge de messages non
  lus) et répond directement depuis chaque fil. Un badge de messages non lus
  apparaît dans le menu, pour l'apprenant comme pour le formateur.
- **Espace « Mes attestations »** (`/comptes/mon-espace/mes-attestations/`) :
  quand le formateur enregistre une attestation dont le prénom/nom correspond
  exactement (et sans ambiguïté) à un compte apprenant existant, l'attestation
  est **automatiquement reliée** à ce compte. En cas d'homonymie ou si le
  compte est créé après coup, l'apprenant peut relier lui-même son attestation
  en saisissant son numéro complet depuis cette page.
- **Logo Web Academy** intégré dans l'en-tête du site et en favicon de l'onglet
  (`core/static/core/img/`).

## 8. Évolutions possibles

- Génération automatique du PDF d'attestation avec QR code
- Multilingue (français / anglais)
