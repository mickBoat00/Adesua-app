# Generated by Django 4.0.6 on 2022-08-26 20:21

import apps.students.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseenrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_enrolled', to='users.student', validators=[apps.students.validators.validate_user_type]),
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together={('course', 'student', 'is_active')},
        ),
    ]
