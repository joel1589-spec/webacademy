import io

import qrcode
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import RechercheAttestationForm
from .models import Attestation, Formation


def accueil(request):
    """Page publique de recherche (section 4.1.1 du cahier des charges)."""
    form = RechercheAttestationForm()
    return render(request, 'attestations/accueil.html', {'form': form})


def verifier(request):
    """
    Page de résultat de la vérification (section 4.1.2).
    La recherche se fait en GET pour permettre le partage direct d'un lien
    de vérification (ex : sur un CV ou LinkedIn) — voir section 3.
    """
    numero = (request.GET.get('numero') or '').strip().upper()
    attestation = None
    trouvee = False

    if numero:
        attestation = Attestation.objects.filter(numero_attestation=numero).select_related('formation').first()
        trouvee = attestation is not None

    contexte = {
        'numero_recherche': numero,
        'attestation': attestation,
        'trouvee': trouvee,
    }
    return render(request, 'attestations/resultat.html', contexte)


def qr_code(request, numero):
    """
    Génère à la volée l'image PNG du QR code pointant vers la page de
    vérification de l'attestation `numero`. Utilisé dans l'admin (pour que
    le formateur puisse le télécharger et le coller sur le PDF de
    l'attestation) et pourra aussi servir à une génération PDF automatique.
    """
    attestation = get_object_or_404(Attestation, numero_attestation=numero.strip().upper())
    image = qrcode.make(attestation.url_verification)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')


def a_propos(request):
    """Page 'À propos de Web Academy' (section 4.1.3)."""
    return render(request, 'attestations/a_propos.html')


def mentions_legales(request):
    """Mentions légales / confidentialité (section 4.1.4)."""
    return render(request, 'attestations/mentions_legales.html')


@staff_member_required
def tableau_de_bord(request):
    """
    Petit tableau de bord de statistiques pour le formateur (section 4.2.6).
    Réservé aux comptes staff/admin connectés via l'authentification Django.
    """
    total = Attestation.objects.count()
    total_valides = Attestation.objects.filter(statut=Attestation.STATUT_VALIDE).count()
    total_revoquees = Attestation.objects.filter(statut=Attestation.STATUT_REVOQUEE).count()

    par_formation = (
        Attestation.objects.values('formation__nom')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    par_session = (
        Attestation.objects.values('annee_session', 'numero_session', 'session_label')
        .annotate(total=Count('id'))
        .order_by('-annee_session', '-numero_session')
    )

    contexte = {
        'total': total,
        'total_valides': total_valides,
        'total_revoquees': total_revoquees,
        'par_formation': par_formation,
        'par_session': par_session,
        'nombre_formations': Formation.objects.count(),
    }
    return render(request, 'attestations/tableau_de_bord.html', contexte)
