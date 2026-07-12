import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attestations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(blank=True, max_length=30, verbose_name='Téléphone')),
                ('ville', models.CharField(blank=True, max_length=100, verbose_name='Ville')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profils/', verbose_name='Photo de profil')),
                ('bio', models.TextField(blank=True, verbose_name='À propos de moi')),
                ('date_inscription', models.DateTimeField(auto_now_add=True, verbose_name='Inscrit le')),
                ('formations_suivies', models.ManyToManyField(blank=True, help_text='Formations auxquelles cet apprenant est inscrit (donne accès aux ressources associées).', related_name='etudiants', to='attestations.formation', verbose_name='Formations suivies')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='etudiant', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Apprenant',
                'verbose_name_plural': 'Apprenants',
                'ordering': ['-date_inscription'],
            },
        ),
    ]
