import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attestations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ressource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200, verbose_name='Titre')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('type_ressource', models.CharField(choices=[('Document', 'Document (PDF, support de cours...)'), ('Video', 'Vidéo'), ('Lien', 'Lien externe')], default='Document', max_length=20, verbose_name='Type')),
                ('fichier', models.FileField(blank=True, null=True, upload_to='ressources/fichiers/', verbose_name='Fichier')),
                ('lien', models.URLField(blank=True, verbose_name='Lien (vidéo ou site externe)')),
                ('date_ajout', models.DateTimeField(auto_now_add=True, verbose_name='Ajoutée le')),
                ('ordre', models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")),
                ('formation', models.ForeignKey(blank=True, help_text="Laisser vide pour rendre la ressource visible par tous les apprenants inscrits.", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ressources', to='attestations.formation', verbose_name='Formation concernée')),
            ],
            options={
                'verbose_name': 'Ressource',
                'verbose_name_plural': 'Ressources',
                'ordering': ['ordre', '-date_ajout'],
            },
        ),
    ]
