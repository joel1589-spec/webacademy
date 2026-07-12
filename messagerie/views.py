from django.contrib import messages as django_messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from comptes.models import Etudiant

from .models import Conversation, Message


@login_required(login_url='comptes:connexion')
def ma_conversation(request):
    """
    Fil de discussion de l'apprenant connecté avec le formateur.
    (Les comptes staff/formateur sont redirigés vers leur propre boîte de réception.)
    """
    if request.user.is_staff:
        return redirect('messagerie:liste_conversations')

    etudiant, _ = Etudiant.objects.get_or_create(user=request.user)
    conversation, _ = Conversation.objects.get_or_create(etudiant=etudiant)

    if request.method == 'POST':
        contenu = (request.POST.get('contenu') or '').strip()
        if contenu:
            Message.objects.create(conversation=conversation, expediteur=request.user, contenu=contenu)
            return redirect('messagerie:ma_conversation')
        django_messages.error(request, "Le message ne peut pas être vide.")

    # Marquer comme lus les messages envoyés par le formateur
    conversation.messages.filter(expediteur__is_staff=True, lu=False).update(lu=True)

    contexte = {'conversation': conversation, 'fil': conversation.messages.select_related('expediteur')}
    return render(request, 'messagerie/ma_conversation.html', contexte)


@staff_member_required
def liste_conversations(request):
    """Boîte de réception du formateur : une ligne par apprenant ayant écrit."""
    conversations = (
        Conversation.objects.select_related('etudiant__user')
        .prefetch_related('messages')
        .order_by('-date_dernier_message')
    )
    lignes = []
    for conversation in conversations:
        dernier = conversation.messages.last()
        non_lus = conversation.messages.filter(expediteur__is_staff=False, lu=False).count()
        lignes.append({'conversation': conversation, 'dernier': dernier, 'non_lus': non_lus})

    return render(request, 'messagerie/liste_conversations.html', {'lignes': lignes})


@staff_member_required
def conversation_detail(request, conversation_id):
    """Vue détaillée d'une conversation, avec réponse possible par le formateur."""
    conversation = get_object_or_404(Conversation, pk=conversation_id)

    if request.method == 'POST':
        contenu = (request.POST.get('contenu') or '').strip()
        if contenu:
            Message.objects.create(conversation=conversation, expediteur=request.user, contenu=contenu)
            return redirect('messagerie:conversation_detail', conversation_id=conversation.id)
        django_messages.error(request, "Le message ne peut pas être vide.")

    conversation.messages.filter(expediteur__is_staff=False, lu=False).update(lu=True)

    contexte = {'conversation': conversation, 'fil': conversation.messages.select_related('expediteur')}
    return render(request, 'messagerie/conversation_detail.html', contexte)
