from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from annonces.models import Annonce
from attestations.models import Attestation, Formation
from blog.models import Article
from comptes.models import Etudiant
from messagerie.models import Conversation, Message
from ressources.models import Ressource
from services.models import Service


class Command(BaseCommand):
    help = (
        "Crée du contenu de démonstration pour l'ensemble du site "
        "(services, annonces, articles de blog, ressources, un compte apprenant de test)."
    )

    def handle(self, *args, **options):
        formation, _ = Formation.objects.get_or_create(
            nom="Développement Web (HTML, CSS, JavaScript)"
        )

        # --- Services -------------------------------------------------------
        services = [
            ("🎓", "Formations pratiques", "Des sessions courtes et intensives en développement web, bureautique et outils digitaux, orientées projets concrets."),
            ("🧑‍🏫", "Accompagnement personnalisé", "Un suivi individuel pendant et après la formation pour répondre à vos questions et débloquer vos projets."),
            ("💼", "Aide à l'insertion", "Des conseils pour préparer un CV, un portfolio, et se présenter aux recruteurs à l'issue de la formation."),
            ("📜", "Attestations vérifiables", "Chaque attestation délivrée est vérifiable en ligne par un numéro unique, pour renforcer votre crédibilité."),
        ]
        for i, (icone, titre, description) in enumerate(services):
            Service.objects.get_or_create(
                titre=titre, defaults={'icone': icone, 'description': description, 'ordre': i}
            )

        # --- Annonces ---------------------------------------------------------
        Annonce.objects.get_or_create(
            titre="Ouverture des inscriptions — Session 2 (Développement Web)",
            defaults={
                'contenu': (
                    "Web Academy ouvre les inscriptions pour sa deuxième session de formation en "
                    "développement web (HTML, CSS, JavaScript). Places limitées, contactez-nous "
                    "rapidement pour réserver votre place."
                ),
                'epinglee': True,
            },
        )
        Annonce.objects.get_or_create(
            titre="Nouvelles ressources disponibles dans votre espace",
            defaults={
                'contenu': (
                    "De nouveaux supports de cours et exercices pratiques ont été ajoutés à l'espace "
                    "ressources. Connectez-vous à votre compte pour les consulter."
                ),
            },
        )

        # --- Articles de blog ---------------------------------------------------
        Article.objects.get_or_create(
            titre="5 conseils pour bien démarrer en développement web",
            defaults={
                'resume': "Nos meilleurs conseils pour progresser rapidement quand on débute en HTML, CSS et JavaScript.",
                'contenu': (
                    "Se lancer dans le développement web peut sembler impressionnant, mais avec de la "
                    "régularité et les bonnes pratiques, les progrès arrivent vite.\n\n"
                    "1. Pratiquez chaque jour, même 30 minutes.\n"
                    "2. Construisez de petits projets plutôt que de multiplier les tutoriels.\n"
                    "3. Apprenez à lire la documentation officielle.\n"
                    "4. Rejoignez une communauté pour poser vos questions.\n"
                    "5. Soyez patient avec les bugs : ils font partie de l'apprentissage."
                ),
                'categorie': "Conseils",
            },
        )
        Article.objects.get_or_create(
            titre="Pourquoi vérifier une attestation de formation ?",
            defaults={
                'resume': "Ce que la vérification en ligne apporte aux recruteurs et aux anciens apprenants.",
                'contenu': (
                    "Une attestation vérifiable en ligne rassure les recruteurs sur l'authenticité du "
                    "parcours suivi par un candidat. Chez Web Academy, chaque attestation délivrée porte "
                    "un numéro unique consultable sur notre site de vérification, sans qu'aucune donnée "
                    "sensible ne soit exposée publiquement."
                ),
                'categorie': "Actualités",
            },
        )

        # --- Ressources ---------------------------------------------------------
        Ressource.objects.get_or_create(
            titre="Support de cours — Bases du HTML/CSS",
            defaults={
                'description': "Le support complet utilisé pendant la session 1, à consulter à votre rythme.",
                'formation': formation,
                'type_ressource': Ressource.TYPE_DOCUMENT,
            },
        )
        Ressource.objects.get_or_create(
            titre="Guide : bonnes pratiques JavaScript",
            defaults={
                'description': "Un lien externe recommandé pour approfondir les fondamentaux de JavaScript.",
                'lien': "https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide",
                'type_ressource': Ressource.TYPE_LIEN,
            },
        )

        # --- Compte apprenant de démonstration -----------------------------------
        if not User.objects.filter(username="demo.etudiant").exists():
            user = User.objects.create_user(
                username="demo.etudiant",
                email="demo.etudiant@example.com",
                password="WebAcademy2026!",
                first_name="Adama",
                last_name="Kossi",
            )
            etudiant = Etudiant.objects.create(user=user, ville="Kara")
            etudiant.formations_suivies.add(formation)
            self.stdout.write(self.style.SUCCESS(
                "Compte apprenant de démonstration créé : demo.etudiant / WebAcademy2026!"
            ))

            # Attestation de démonstration : le prénom/nom correspondent exactement
            # à ceux du compte ci-dessus, donc la liaison à "Mes attestations" se
            # fait automatiquement (voir Attestation._tenter_liaison_automatique).
            if not Attestation.objects.filter(prenom="Adama", nom="Kossi").exists():
                Attestation.objects.create(
                    prenom="Adama",
                    nom="Kossi",
                    formation=formation,
                    date_debut=timezone.datetime(2026, 7, 13).date(),
                    date_fin=timezone.datetime(2026, 8, 13).date(),
                    volume_horaire=45,
                    session_label="Session 1 - Vogan",
                    afficher_nom_complet=True,
                )
                self.stdout.write(self.style.SUCCESS(
                    "Attestation de démonstration créée et reliée automatiquement au compte demo.etudiant."
                ))

            # Premier message de démonstration dans la messagerie interne, pour
            # que le formateur voie immédiatement une conversation en attente.
            conversation, _ = Conversation.objects.get_or_create(etudiant=etudiant)
            if not conversation.messages.exists():
                Message.objects.create(
                    conversation=conversation,
                    expediteur=user,
                    contenu=(
                        "Bonjour, je viens de terminer la formation Développement Web. "
                        "Est-ce que mon attestation est bien disponible ? Merci !"
                    ),
                )
                self.stdout.write(self.style.SUCCESS(
                    "Message de démonstration envoyé dans la messagerie interne."
                ))

        self.stdout.write(self.style.SUCCESS("Contenu de démonstration créé avec succès."))
