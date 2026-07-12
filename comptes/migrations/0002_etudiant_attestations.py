from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attestations', '0001_initial'),
        ('comptes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='attestations',
            field=models.ManyToManyField(
                blank=True,
                help_text=(
                    "Attestations rattachées à ce compte apprenant (liaison automatique par "
                    "correspondance de nom, ou ajoutées manuellement par l'apprenant via son numéro)."
                ),
                related_name='apprenants',
                to='attestations.attestation',
                verbose_name='Attestations liées',
            ),
        ),
    ]
