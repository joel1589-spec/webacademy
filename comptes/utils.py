import unicodedata


def normaliser(texte):
    """
    Normalise un nom pour comparaison : minuscules, sans accents, sans espaces
    superflus. Permet de faire correspondre "Kokou" et "kokou", "Ayélé" et
    "Ayele", etc.
    """
    texte = texte or ""
    texte = unicodedata.normalize('NFKD', texte).encode('ascii', 'ignore').decode('ascii')
    return texte.strip().lower()


def tenter_liaison_pour_attestation(attestation):
    """
    À la création d'une attestation, cherche s'il existe UN SEUL compte
    apprenant dont le prénom + nom correspond exactement (une fois normalisé)
    à celui de l'attestation, et les relie automatiquement.

    Ne fait rien en cas d'ambiguïté (plusieurs apprenants portant le même nom) :
    l'apprenant pourra toujours associer l'attestation manuellement avec son
    numéro depuis "Mes attestations".
    """
    from comptes.models import Etudiant

    cible = (normaliser(attestation.prenom), normaliser(attestation.nom))
    candidats = [
        etudiant for etudiant in Etudiant.objects.select_related('user').all()
        if (normaliser(etudiant.user.first_name), normaliser(etudiant.user.last_name)) == cible
    ]
    if len(candidats) == 1:
        candidats[0].attestations.add(attestation)


def tenter_liaison_pour_etudiant(etudiant):
    """
    À la création d'un compte apprenant, cherche s'il existe UNE SEULE
    attestation déjà délivrée à ce nom et la relie automatiquement.
    """
    from attestations.models import Attestation

    cible = (normaliser(etudiant.user.first_name), normaliser(etudiant.user.last_name))
    candidats = [
        attestation for attestation in Attestation.objects.all()
        if (normaliser(attestation.prenom), normaliser(attestation.nom)) == cible
    ]
    if len(candidats) == 1:
        etudiant.attestations.add(candidats[0])
