from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from annonces.models import Annonce
from attestations.models import Attestation
from ressources.models import Ressource

from .forms import InscriptionForm, LierAttestationForm, ProfilForm
from .models import Etudiant


def inscription(request):
    """Création d'un compte apprenant (section : espace personnel apprenant)."""
    if request.user.is_authenticated:
        return redirect('comptes:mon_espace')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Bienvenue chez Web Academy, {user.first_name} ! Votre compte a été créé.")
            return redirect('comptes:mon_espace')
    else:
        form = InscriptionForm()

    return render(request, 'comptes/inscription.html', {'form': form})


class ConnexionView(LoginView):
    """Connexion des apprenants (les formateurs/administrateurs utilisent /admin/)."""

    template_name = 'comptes/connexion.html'
    redirect_authenticated_user = True


def deconnexion(request):
    auth_logout(request)
    messages.info(request, "Vous avez été déconnecté. À bientôt !")
    return redirect('core:accueil')


@login_required(login_url='comptes:connexion')
def mon_espace(request):
    """Tableau de bord personnel de l'apprenant connecté."""
    etudiant, _ = Etudiant.objects.get_or_create(user=request.user)

    formations = etudiant.formations_suivies.all()
    ressources = (
        Ressource.objects.filter(formation__in=formations) | Ressource.objects.filter(formation__isnull=True)
    ).distinct().order_by('-date_ajout')[:8]

    dernieres_annonces = Annonce.objects.order_by('-epinglee', '-date_publication')[:3]

    contexte = {
        'etudiant': etudiant,
        'formations': formations,
        'ressources': ressources,
        'annonces': dernieres_annonces,
    }
    return render(request, 'comptes/mon_espace.html', contexte)


@login_required(login_url='comptes:connexion')
def modifier_profil(request):
    etudiant, _ = Etudiant.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=etudiant, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour.")
            return redirect('comptes:mon_espace')
    else:
        form = ProfilForm(instance=etudiant, user=request.user)

    return render(request, 'comptes/modifier_profil.html', {'form': form})


@login_required(login_url='comptes:connexion')
def mes_attestations(request):
    """
    Espace "Mes attestations" : liste les attestations déjà reliées
    automatiquement au compte (par correspondance de nom), et permet à
    l'apprenant d'en associer manuellement d'autres avec leur numéro exact.
    """
    etudiant, _ = Etudiant.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = LierAttestationForm(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['numero_attestation'].strip().upper()
            attestation = Attestation.objects.filter(numero_attestation=numero).first()
            if attestation is None:
                messages.error(request, "Aucune attestation ne correspond à ce numéro. Vérifiez la saisie.")
            elif etudiant.attestations.filter(pk=attestation.pk).exists():
                messages.info(request, "Cette attestation est déjà associée à votre compte.")
            else:
                etudiant.attestations.add(attestation)
                messages.success(request, f"L'attestation {attestation.numero_attestation} a été associée à votre compte.")
            return redirect('comptes:mes_attestations')
    else:
        form = LierAttestationForm()

    contexte = {
        'etudiant': etudiant,
        'attestations': etudiant.attestations.select_related('formation').all(),
        'form': form,
    }
    return render(request, 'comptes/mes_attestations.html', contexte)
