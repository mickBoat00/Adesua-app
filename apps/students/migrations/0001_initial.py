# Generated by Django 4.0.6 on 2022-08-17 17:37

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))], verbose_name='Price')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='course.course')),
            ],
        ),
    ]
