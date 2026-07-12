from django.contrib import admin

from .models import Etudiant


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user_email', 'telephone', 'ville', 'date_inscription')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'telephone', 'ville')
    list_filter = ('formations_suivies', 'ville')
    filter_horizontal = ('formations_suivies', 'attestations')

    @admin.display(description="Email")
    def user_email(self, obj):
        return obj.user.email
