from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Etudiant


class InscriptionForm(UserCreationForm):
    """Formulaire d'inscription d'un apprenant : crée un compte User + un profil Etudiant."""

    first_name = forms.CharField(label="Prénom", max_length=100, required=True)
    last_name = forms.CharField(label="Nom", max_length=100, required=True)
    email = forms.EmailField(label="Adresse email", required=True)
    telephone = forms.CharField(label="Téléphone", max_length=30, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Un compte existe déjà avec cette adresse email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Etudiant.objects.create(
                user=user,
                telephone=self.cleaned_data.get('telephone', ''),
            )
        return user


class ProfilForm(forms.ModelForm):
    """Modification du profil apprenant (informations complémentaires)."""

    first_name = forms.CharField(label="Prénom", max_length=100)
    last_name = forms.CharField(label="Nom", max_length=100)
    email = forms.EmailField(label="Adresse email")

    class Meta:
        model = Etudiant
        fields = ['telephone', 'ville', 'photo', 'bio']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user
        if user is not None:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        etudiant = super().save(commit=False)
        if self._user is not None:
            self._user.first_name = self.cleaned_data['first_name']
            self._user.last_name = self.cleaned_data['last_name']
            self._user.email = self.cleaned_data['email']
            if commit:
                self._user.save()
        if commit:
            etudiant.save()
        return etudiant


class LierAttestationForm(forms.Form):
    """Permet à un apprenant d'associer manuellement une attestation à son compte,
    en saisissant le numéro complet inscrit sur son document."""

    numero_attestation = forms.CharField(
        label="Numéro d'attestation",
        max_length=40,
        widget=forms.TextInput(attrs={'placeholder': 'Ex : WA-2026-S1-014-7X2K'}),
    )
