from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.course.models import Category, Course


class Command(BaseCommand):
    help = 'Populates the database with some data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Started database population process...'))

        if Category.objects.filter(name='Django').exists():
            self.stdout.write(self.style.SUCCESS('Database has already been populated. Cancelling the operation.'))
            return

        with transaction.atomic():

            cat1 = Category.objects.create(name='Django')
            cat2 = Category.objects.create(name='PostgreSQL')
            cat3 = Category.objects.create(name='React')

            course1 = Course.objects.create(
                instructor_id = 1,
                title = "Intro To Django",
                slug = "intro-to-django",
                description = "dnie diendeni",
                cover_image = "http://localhost:8000/media/course_images/interior_sample_Ihb2hNb.jpg",
                price = "0.00",
                rating = "0.00",
                raters = 0,
                pay = "Free",
                published_status = True
            )

            course1.categories.add(cat1)


        self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))