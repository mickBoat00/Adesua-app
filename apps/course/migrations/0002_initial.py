# Generated by Django 4.0.6 on 2022-09-02 16:52

import apps.course.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='users.courseinstructor', validators=[apps.course.validators.validate_user_type], verbose_name='Course Instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.year', verbose_name='Class Level'),
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('course', 'title')},
        ),
    ]
