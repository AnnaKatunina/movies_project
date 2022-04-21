# Generated by Django 3.2 on 2022-02-20 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_added_genres_persons_to_filmworks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personfilmwork',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_film_works', to='movies.person', verbose_name='person'),
        ),
    ]
