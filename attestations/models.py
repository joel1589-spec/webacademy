import random
import string

from django.db import models
from django.utils import timezone


def annee_courante():
    return timezone.now().year


class Formation(models.Model):
    """Une formation proposée par Web Academy (liste déroulante extensible)."""

    nom = models.CharField(
        "Intitulé de la formation",
        max_length=200,
        unique=True,
        help_text="Ex : Développement Web (HTML, CSS, JavaScript)",
    )

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Attestation(models.Model):
    """Une attestation de fin de formation délivrée à un apprenant."""

    STATUT_VALIDE = 'Valide'
    STATUT_REVOQUEE = 'Revoquee'
    STATUT_CHOICES = [
        (STATUT_VALIDE, 'Valide'),
        (STATUT_REVOQUEE, 'Révoquée'),
    ]

    # Identifiant public, généré automatiquement (voir section 5 du cahier des charges)
    numero_attestation = models.CharField(
        "Numéro d'attestation",
        max_length=40,
        unique=True,
        blank=True,
        help_text="Généré automatiquement à l'enregistrement (ex : WA-2026-S1-014-7X2K).",
    )

    prenom = models.CharField("Prénom", max_length=100)
    nom = models.CharField("Nom", max_length=100)

    formation = models.ForeignKey(
        Formation,
        on_delete=models.PROTECT,
        related_name='attestations',
        verbose_name="Formation suivie",
    )

    date_debut = models.DateField("Date de début de la formation")
    date_fin = models.DateField("Date de fin de la formation")
    volume_horaire = models.PositiveIntegerField("Volume horaire (heures)")
    date_delivrance = models.DateField("Date de délivrance de l'attestation", default=timezone.now)

    # Utilisés pour construire le numéro d'attestation (WA-<annee>-S<numero_session>-...)
    annee_session = models.PositiveIntegerField("Année de la session", default=annee_courante)
    numero_session = models.PositiveIntegerField(
        "Numéro de session",
        default=1,
        help_text="Ex : 1 pour la 1ère session (deviendra S1 dans le numéro).",
    )
    session_label = models.CharField(
        "Nom de la session",
        max_length=150,
        blank=True,
        help_text="Ex : Session 1 - Vogan",
    )

    statut = models.CharField(
        "Statut", max_length=20, choices=STATUT_CHOICES, default=STATUT_VALIDE
    )

    afficher_nom_complet = models.BooleanField(
        "Afficher le nom complet",
        default=False,
        help_text=(
            "Cocher uniquement si l'apprenant a donné son accord écrit pour l'affichage "
            "de son nom complet. Sinon, seule l'initiale du nom sera affichée."
        ),
    )

    date_creation = models.DateTimeField("Créée le", auto_now_add=True)
    date_modification = models.DateTimeField("Modifiée le", auto_now=True)

    class Meta:
        verbose_name = "Attestation"
        verbose_name_plural = "Attestations"
        ordering = ['-date_delivrance', '-id']

    def __str__(self):
        return f"{self.numero_attestation} — {self.prenom} {self.nom}"

    # --- Génération du numéro unique ------------------------------------------------

    def save(self, *args, **kwargs):
        if not self.numero_attestation:
            self.numero_attestation = self._generer_numero()
        super().save(*args, **kwargs)
        self._tenter_liaison_automatique()

    def _tenter_liaison_automatique(self):
        """
        Tente de relier automatiquement cette attestation à un compte apprenant
        existant, en comparant le prénom et le nom saisis (insensible à la casse).
        Si plusieurs comptes correspondent (ex : homonymes), aucune liaison
        automatique n'est faite : l'apprenant peut toujours relier lui-même son
        attestation depuis son espace « Mes attestations » via le numéro complet,
        et le formateur peut aussi le faire manuellement depuis l'admin.
        """
        if self.apprenants.exists():
            return

        from django.apps import apps

        Etudiant = apps.get_model('comptes', 'Etudiant')
        candidats = Etudiant.objects.filter(
            user__first_name__iexact=self.prenom.strip(),
            user__last_name__iexact=self.nom.strip(),
        )
        if candidats.count() == 1:
            candidats.first().attestations.add(self)

    def _generer_numero(self):
        """
        Construit un numéro au format WA-<annee>-S<session>-<sequence>-<code_aleatoire>.
        Le code aléatoire final empêche de deviner un numéro par simple incrémentation
        (voir section 5 du cahier des charges, option 2).
        """
        sequence = (
            Attestation.objects.filter(
                annee_session=self.annee_session,
                numero_session=self.numero_session,
            ).count()
            + 1
        )
        alphabet = string.ascii_uppercase + string.digits
        # on retire les caractères ambigus (0/O, 1/I) pour limiter les erreurs de saisie
        alphabet = alphabet.translate(str.maketrans('', '', '01OI'))
        code_aleatoire = ''.join(random.choices(alphabet, k=4))

        numero = (
            f"WA-{self.annee_session}-S{self.numero_session}-"
            f"{sequence:03d}-{code_aleatoire}"
        )
        # Filet de sécurité en cas de collision improbable
        while Attestation.objects.filter(numero_attestation=numero).exists():
            code_aleatoire = ''.join(random.choices(alphabet, k=4))
            numero = (
                f"WA-{self.annee_session}-S{self.numero_session}-"
                f"{sequence:03d}-{code_aleatoire}"
            )
        return numero

    # --- Affichage public (protection des données personnelles, section 7) -------

    @property
    def nom_affiche(self):
        if self.afficher_nom_complet:
            return f"{self.prenom} {self.nom}"
        initiale = f"{self.nom[0]}." if self.nom else ""
        return f"{self.prenom} {initiale}".strip()

    @property
    def est_valide(self):
        return self.statut == self.STATUT_VALIDE

    # --- QR code de vérification (section 8, PDF d'attestation) ---------------------

    @property
    def url_verification(self):
        """
        Lien absolu vers la page publique de vérification de cette attestation
        précise (pré-rempli avec son numéro). C'est ce lien qui est encodé dans
        le QR code à coller sur le PDF de l'attestation.
        """
        from django.conf import settings
        from django.urls import reverse

        chemin = reverse('attestations:verifier')
        return f"{settings.SITE_URL}{chemin}?numero={self.numero_attestation}"
