# Generated by Django 4.0.6 on 2022-08-13 04:40

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='+233559875250', max_length=30, region=None, verbose_name='Phone Number')),
                ('about_me', models.TextField(default='say something about yourself', verbose_name='About me')),
                ('profile_photo', models.ImageField(default='/profile_default.png', upload_to='', verbose_name='Profile Photo')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other', max_length=20, verbose_name='Gender')),
                ('country', models.CharField(default='Ghana', max_length=100, verbose_name='Country')),
                ('city', models.CharField(default='Accra', max_length=180, verbose_name='City')),
                ('website', models.URLField(blank=True, null=True, verbose_name='My Website')),
                ('twitter', models.URLField(blank=True, null=True, verbose_name='My Twitter')),
                ('youtube', models.URLField(blank=True, null=True, verbose_name='My Youtube')),
                ('num_reviews', models.IntegerField(blank=True, default=0, null=True, verbose_name='Number of Reviews')),
                ('num_students', models.IntegerField(blank=True, default=0, null=True, verbose_name='Number of Students')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
