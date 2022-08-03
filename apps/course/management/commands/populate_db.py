import random

import faker.providers
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

User = get_user_model()

from apps.course.models import Category, Course, Lesson

CATEGORIES = [
    "Django",
    "Django Rest Framework",
    "React",
    "Machine Learning",
    "DevOps",
    "Docker",
    "Nginx",
]


COURSE_TITLE = [
    "Introduction to Twi",
    "Introduction to Basket Weaving",
    "Introduction to Basket Weaving",
]

LESSON_TITLE = [
    "Lesson One",
    "Lesson Two",
    "Lesson Three",
]


class Provider(faker.providers.BaseProvider):
    def course_category(self):
        return self.random_element(CATEGORIES)

    def lesson_title(self):
        return self.random_element(LESSON_TITLE)


class Command(BaseCommand):
    help = "Populate the database with some data"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        fake = Faker("tw_GH")
        fake.add_provider(Provider)

        # Create three users
        for _ in range(3):
            first_name = (fake.first_name(),)
            last_name = (fake.last_name(),)
            email = (f"{first_name[0]}-{last_name[0]}@gmail.com",)

            user = User.objects.create_user(
                first_name=first_name[0],
                username=first_name[0],
                last_name=last_name[0],
                email=email[0],
                password="testing321",
            )
            user.is_active = True

        # Create a number of categories
        for _ in range(len(CATEGORIES)):
            data = fake.unique.course_category()
            Category.objects.create(name=data)

        check_category = Category.objects.all().count()
        self.stdout.write(self.style.SUCCESS(f"Number of categories: {check_category}"))

        # Create 10 courses with three lessons each
        pay = ["Paid", "Free"]
        for _ in range(10):

            course = Course.objects.create(
                instructor_id=1,
                title=fake.text(max_nb_chars=15),
                description=fake.text(max_nb_chars=50),
                cover_image="http://localhost:8000/media/course_images/interior_sample_Ihb2hNb.jpg",
                price=(round(random.uniform(9.99, 99.99), 2)),
                pay=random.choice(pay),
                published_status=True,
            )

            for i in range(len(LESSON_TITLE)):

                Lesson.objects.create(course_id=course.id, title=LESSON_TITLE[i], description="I love what this it")


"""
    Create users should be assigned courses
    Create default users or instrcutors 
    Lesson needed to have some videos
"""
