from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=150, verbose_name='Titre')),
                ('description', models.TextField(verbose_name='Description')),
                ('icone', models.CharField(default='🎓', help_text='Un emoji simple à afficher devant le titre, ex : 🎓 💻 🧑\u200d🏫', max_length=10, verbose_name='Icône (emoji)')),
                ('ordre', models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")),
                ('actif', models.BooleanField(default=True, verbose_name='Visible sur le site')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'ordering': ['ordre', 'titre'],
            },
        ),
    ]
