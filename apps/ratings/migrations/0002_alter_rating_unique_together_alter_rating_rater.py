# Generated by Django 4.0.6 on 2022-07-28 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_initial'),
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rater',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.profile', unique=True, verbose_name='Enrolled Student providing the rating'),
        ),
    ]
