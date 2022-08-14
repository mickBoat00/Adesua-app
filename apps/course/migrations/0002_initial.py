# Generated by Django 4.0.6 on 2022-08-13 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='course.course'),
        ),
        migrations.AddField(
            model_name='course',
            name='curriculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.curriculum', verbose_name='Course Syllables'),
        ),
    ]
