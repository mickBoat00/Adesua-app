# Generated by Django 4.0.6 on 2022-08-11 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_alter_course_instructor_alter_lesson_video'),
        ('ratings', '0002_alter_rating_course_alter_rating_rater'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ratings', to='course.course', verbose_name='Course being rated'),
        ),
    ]