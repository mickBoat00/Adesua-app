# Generated by Django 4.0.6 on 2022-08-06 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_alter_year_value'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('-created_on',), 'verbose_name': 'Course', 'verbose_name_plural': 'Courses'},
        ),
    ]