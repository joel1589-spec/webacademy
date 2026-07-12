import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comptes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Créée le')),
                ('date_dernier_message', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Dernier message le')),
                ('etudiant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='conversation', to='comptes.etudiant', verbose_name='Apprenant')),
            ],
            options={
                'verbose_name': 'Conversation',
                'verbose_name_plural': 'Conversations',
                'ordering': ['-date_dernier_message'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField(verbose_name='Message')),
                ('date_envoi', models.DateTimeField(auto_now_add=True, verbose_name='Envoyé le')),
                ('lu', models.BooleanField(default=False, verbose_name='Lu par le destinataire')),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='messagerie.conversation', verbose_name='Conversation')),
                ('expediteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_envoyes', to=settings.AUTH_USER_MODEL, verbose_name='Expéditeur')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['date_envoi'],
            },
        ),
    ]
