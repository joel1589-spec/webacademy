from django.contrib import admin

from .models import Choix, Copie, Question, ReponseAcceptee, ReponseEtudiant, Sujet


class ChoixInline(admin.TabularInline):
    model = Choix
    extra = 2
    fields = ('texte', 'est_correct', 'ordre')


class ReponseAccepteeInline(admin.TabularInline):
    model = ReponseAcceptee
    extra = 1
    fields = ('texte',)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ('ordre', 'type_question', 'enonce', 'points')
    show_change_link = True


@admin.register(Sujet)
class SujetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'duree_minutes', 'nombre_questions', 'note_totale', 'actif', 'date_creation')
    list_filter = ('actif',)
    search_fields = ('titre',)
    inlines = [QuestionInline]

    @admin.display(description="Nb. questions")
    def nombre_questions(self, obj):
        return obj.nombre_questions

    @admin.display(description="Noté sur")
    def note_totale(self, obj):
        return obj.note_totale


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Accessible séparément de Sujet pour pouvoir ajouter les choix de réponse
    et les réponses acceptées (corrigé), impossible à imbriquer sur deux
    niveaux dans l'admin de Sujet.
    """
    list_display = ('sujet', 'ordre', 'type_question', 'enonce_court', 'points')
    list_filter = ('sujet', 'type_question')
    inlines = [ChoixInline, ReponseAccepteeInline]

    @admin.display(description="Énoncé")
    def enonce_court(self, obj):
        return obj.enonce[:70]


class ReponseEtudiantInline(admin.TabularInline):
    model = ReponseEtudiant
    extra = 0
    fields = ('question', 'texte_libre', 'choix_selectionnes', 'points_obtenus')
    readonly_fields = ('question', 'texte_libre', 'choix_selectionnes')
    can_delete = False


@admin.register(Copie)
class CopieAdmin(admin.ModelAdmin):
    """Consultation des copies et de leur note. La correction est automatique ;
    cet écran sert surtout à vérifier/ajuster une note en cas de litige."""
    list_display = ('etudiant', 'sujet', 'date_debut', 'date_soumission', 'terminee', 'note_obtenue', 'note_sur')
    list_filter = ('sujet', 'terminee')
    search_fields = ('etudiant__user__first_name', 'etudiant__user__last_name')
    readonly_fields = ('sujet', 'etudiant', 'date_debut', 'date_soumission', 'terminee')
    inlines = [ReponseEtudiantInline]

    @admin.display(description="Noté sur")
    def note_sur(self, obj):
        return obj.note_sur

    def has_add_permission(self, request):
        return False
