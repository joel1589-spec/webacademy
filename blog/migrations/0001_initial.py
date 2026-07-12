import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200, verbose_name='Titre')),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True, verbose_name='Slug (URL)')),
                ('resume', models.CharField(max_length=300, verbose_name='Résumé (affiché dans la liste)')),
                ('contenu', models.TextField(verbose_name="Contenu de l'article")),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Image de couverture')),
                ('categorie', models.CharField(blank=True, help_text='Ex : Conseils, Actualités, Témoignages', max_length=100, verbose_name='Catégorie')),
                ('publie', models.BooleanField(default=True, verbose_name='Publié')),
                ('date_publication', models.DateTimeField(auto_now_add=True, verbose_name='Publié le')),
                ('auteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='Auteur')),
            ],
            options={
                'verbose_name': 'Article de blog',
                'verbose_name_plural': 'Articles de blog',
                'ordering': ['-date_publication'],
            },
        ),
    ]
