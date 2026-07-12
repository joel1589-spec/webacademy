from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annonce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200, verbose_name='Titre')),
                ('contenu', models.TextField(verbose_name='Contenu')),
                ('image', models.ImageField(blank=True, null=True, upload_to='annonces/', verbose_name='Image (optionnelle)')),
                ('epinglee', models.BooleanField(default=False, help_text='Cocher pour faire apparaître cette annonce en premier.', verbose_name='Épinglée en haut de la liste')),
                ('date_publication', models.DateTimeField(auto_now_add=True, verbose_name='Publiée le')),
            ],
            options={
                'verbose_name': 'Annonce',
                'verbose_name_plural': 'Annonces',
                'ordering': ['-epinglee', '-date_publication'],
            },
        ),
    ]
