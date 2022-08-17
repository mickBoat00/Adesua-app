# Generated by Django 4.0.6 on 2022-08-15 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')], default=0, help_text='1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent', verbose_name='Rating')),
                ('comment', models.TextField(verbose_name='Comment')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ratings', to='course.course', verbose_name='Course being rated')),
            ],
        ),
    ]
