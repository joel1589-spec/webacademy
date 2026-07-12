import csv

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html

from .models import Attestation, Formation


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nombre_attestations')
    search_fields = ('nom',)

    @admin.display(description="Nombre d'attestations délivrées")
    def nombre_attestations(self, obj):
        return obj.attestations.count()


@admin.register(Attestation)
class AttestationAdmin(admin.ModelAdmin):
    list_display = (
        'numero_attestation',
        'prenom',
        'nom',
        'formation',
        'session_label',
        'date_delivrance',
        'statut',
        'comptes_apprenants_lies',
    )
    list_filter = ('statut', 'formation', 'annee_session', 'numero_session')
    search_fields = ('numero_attestation', 'prenom', 'nom', 'session_label')
    readonly_fields = (
        'numero_attestation', 'date_creation', 'date_modification',
        'qr_code_apercu', 'comptes_apprenants_lies',
    )
    date_hierarchy = 'date_delivrance'
    ordering = ('-date_delivrance',)
    actions = ['exporter_csv', 'marquer_revoquee', 'marquer_valide']

    fieldsets = (
        ("Apprenant", {
            'fields': ('prenom', 'nom', 'afficher_nom_complet', 'comptes_apprenants_lies'),
            'description': (
                "La liaison à un compte apprenant se fait automatiquement par nom/prénom, "
                "ou manuellement depuis la fiche « Étudiant » (Comptes → Étudiants)."
            ),
        }),
        ("Formation", {
            'fields': ('formation', 'date_debut', 'date_fin', 'volume_horaire'),
        }),
        ("Session et délivrance", {
            'fields': (
                'session_label', 'annee_session', 'numero_session',
                'date_delivrance', 'statut',
            ),
        }),
        ("Identifiant (généré automatiquement)", {
            'fields': ('numero_attestation', 'date_creation', 'date_modification'),
        }),
        ("QR code de vérification", {
            'fields': ('qr_code_apercu',),
            'description': "À télécharger et coller sur le PDF de l'attestation remis à l'apprenant.",
        }),
    )

    @admin.display(description="QR code")
    def qr_code_apercu(self, obj):
        if not obj.pk:
            return "— enregistrez d'abord l'attestation pour générer son QR code —"
        url_qr = reverse('attestations:qr_code', args=[obj.numero_attestation])
        return format_html(
            '<img src="{}" width="180" height="180" '
            'style="border:1px solid #ccc; padding:6px; background:#fff;"><br>'
            '<a href="{}" download="qr_{}.png">Télécharger le QR code</a><br>'
            '<small>Pointe vers : {}</small>',
            url_qr, url_qr, obj.numero_attestation, obj.url_verification,
        )

    @admin.display(description="Compte(s) apprenant lié(s)")
    def comptes_apprenants_lies(self, obj):
        return ", ".join(str(e) for e in obj.apprenants.all()) or "—"

    @admin.action(description="Exporter la sélection en CSV")
    def exporter_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attestations_webacademy.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Numéro attestation', 'Prénom', 'Nom', 'Formation',
            'Date début', 'Date fin', 'Volume horaire', 'Date délivrance',
            'Session', 'Statut',
        ])
        for a in queryset.select_related('formation'):
            writer.writerow([
                a.numero_attestation, a.prenom, a.nom, a.formation.nom,
                a.date_debut, a.date_fin, a.volume_horaire, a.date_delivrance,
                a.session_label, a.get_statut_display(),
            ])
        return response

    @admin.action(description="Marquer comme Révoquée")
    def marquer_revoquee(self, request, queryset):
        queryset.update(statut=Attestation.STATUT_REVOQUEE)

    @admin.action(description="Marquer comme Valide")
    def marquer_valide(self, request, queryset):
        queryset.update(statut=Attestation.STATUT_VALIDE)
