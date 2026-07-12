from django.db.models.signals import post_save
from django.dispatch import receiver

from attestations.models import Attestation

from .models import Etudiant
from .utils import tenter_liaison_pour_attestation, tenter_liaison_pour_etudiant


@receiver(post_save, sender=Attestation)
def lier_attestation_a_l_etudiant(sender, instance, created, **kwargs):
    """Dès qu'une attestation est créée (via /admin/), tente de la relier automatiquement."""
    if created:
        tenter_liaison_pour_attestation(instance)


@receiver(post_save, sender=Etudiant)
def lier_etudiant_a_ses_attestations(sender, instance, created, **kwargs):
    """Dès qu'un compte apprenant est créé, tente de relier ses attestations existantes."""
    if created:
        tenter_liaison_pour_etudiant(instance)
