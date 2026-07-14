from django.conf import settings
from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from comptes.models import Etudiant

from .models import Conversation, Message
from .services import ErreurAssistantIA, demander_a_l_ia

# Nombre maximum de questions qu'un même apprenant peut poser par jour,
# pour éviter un usage abusif de la clé API (chaque appel a un coût réel).
QUOTA_QUESTIONS_PAR_JOUR = getattr(settings, 'ASSISTANT_QUOTA_QUOTIDIEN', 30)


@login_required(login_url='comptes:connexion')
def mon_assistant(request):
    """Fil de discussion de l'apprenant connecté avec l'assistant IA."""
    etudiant, _ = Etudiant.objects.get_or_create(user=request.user)
    conversation, _ = Conversation.objects.get_or_create(etudiant=etudiant)

    aujourdhui = timezone.localdate()
    questions_du_jour = conversation.messages.filter(
        role=Message.ROLE_ETUDIANT, date_envoi__date=aujourdhui,
    ).count()
    quota_atteint = questions_du_jour >= QUOTA_QUESTIONS_PAR_JOUR

    if request.method == 'POST':
        question = (request.POST.get('contenu') or '').strip()
        if not question:
            django_messages.error(request, "Votre question ne peut pas être vide.")
        elif quota_atteint:
            django_messages.error(
                request,
                f"Vous avez atteint la limite de {QUOTA_QUESTIONS_PAR_JOUR} questions par jour. "
                "Réessayez demain.",
            )
        else:
            historique = list(conversation.messages.all())
            Message.objects.create(conversation=conversation, role=Message.ROLE_ETUDIANT, contenu=question)
            try:
                reponse = demander_a_l_ia(historique, question)
            except ErreurAssistantIA as erreur:
                reponse = f"⚠️ {erreur}"
            Message.objects.create(conversation=conversation, role=Message.ROLE_IA, contenu=reponse)
        return redirect('assistant:mon_assistant')

    contexte = {
        'conversation': conversation,
        'fil': conversation.messages.all(),
        'questions_du_jour': questions_du_jour,
        'quota': QUOTA_QUESTIONS_PAR_JOUR,
        'quota_atteint': quota_atteint,
    }
    return render(request, 'assistant/mon_assistant.html', contexte)
