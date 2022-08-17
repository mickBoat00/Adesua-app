# Generated by Django 4.0.6 on 2022-08-17 17:37

import autoslug.fields
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100, verbose_name='Course Title')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=True, populate_from='title', unique=True)),
                ('description', models.TextField()),
                ('cover_image', models.ImageField(default='default.png', upload_to='course_images', verbose_name='Main Image')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Price')),
                ('pay', models.CharField(choices=[('Free', 'Free'), ('Paid', 'Paid')], default='Free', max_length=4, verbose_name='Paid / Free')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=8, verbose_name='Status')),
                ('published_status', models.BooleanField(default=False, verbose_name='Published Status')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'ordering': ('-created_on',),
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=10, verbose_name='Course Curriculum')),
            ],
            options={
                'verbose_name_plural': 'Curriculum',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100, verbose_name='Lesson Title')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=True, populate_from='title', unique=True)),
                ('description', models.TextField()),
                ('video', models.FileField(upload_to='lesson_videos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])], verbose_name='Lesson Video')),
            ],
            options={
                'verbose_name': 'Lesson',
                'verbose_name_plural': 'Lessons',
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('value', models.CharField(max_length=2, unique=True, verbose_name='School Year')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='course.course')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
