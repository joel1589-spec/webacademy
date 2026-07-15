from django.db import migrations, models

import ressources.models


class Migration(migrations.Migration):

    dependencies = [
        ('ressources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ressource',
            name='fichier',
            field=models.FileField(
                blank=True,
                null=True,
                storage=ressources.models.stockage_fichiers_ressources,
                upload_to='ressources/fichiers/',
                verbose_name='Fichier',
            ),
        ),
    ]
