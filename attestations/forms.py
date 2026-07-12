from django import forms


class RechercheAttestationForm(forms.Form):
    numero = forms.CharField(
        label="Numéro d'attestation",
        max_length=40,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex : WA-2026-S1-014-7X2K',
            'autofocus': 'autofocus',
            'class': 'champ-recherche',
        }),
    )

    def clean_numero(self):
        return self.cleaned_data['numero'].strip().upper()
