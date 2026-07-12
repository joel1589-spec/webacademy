from .models import Message


def compteur_messages(request):
    """
    Rend disponible `nombre_messages_non_lus` dans tous les templates, pour
    afficher un badge dans le menu (ex : "Messagerie (2)").
    """
    if not request.user.is_authenticated:
        return {}

    if request.user.is_staff:
        # Messages envoyés par des apprenants, pas encore lus par le formateur.
        nombre = Message.objects.filter(expediteur__is_staff=False, lu=False).count()
    else:
        # Messages envoyés par le formateur à CET apprenant, pas encore lus.
        nombre = Message.objects.filter(
            conversation__etudiant__user=request.user, expediteur__is_staff=True, lu=False
        ).count()

    return {'nombre_messages_non_lus': nombre}
