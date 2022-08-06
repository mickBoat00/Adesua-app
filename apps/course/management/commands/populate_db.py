import random

import faker.providers
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

User = get_user_model()

from apps.course.models import Course, Curriculum, Lesson, Year
from apps.profiles.models import Profile

CURRICULUM_LIST = [
    "AICE",
    "A Levels",
    "FrBacc",
    "IPC",
    "USA",
    "UK",
    "IBDP",
    "IBMYP",
    "IBPYP",
    "IBCP",
    "IGCSE",
    "GCSE",
    "Natl",
    "AP",
    "SAT",
]


YEAR_LIST = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
]

COURSE_TITLE = [
    "English",
    "Mathematics",
    "Social Studies",
    "Science",
    "History",
    "French",
    "Ghanaian Language",
    "Spanish",
    "Spanish",
    "Religious And Morals Educations",
    "Music and Dance",
]

LESSON_TITLE = [
    "Lesson One",
    "Lesson Two",
    "Lesson Three",
    "Lesson Four",
]


class Provider(faker.providers.BaseProvider):
    def course_curriculum(self):
        return self.random_element(CURRICULUM_LIST)

    def year_list(self):
        return self.random_element(YEAR_LIST)

    def lesson_title(self):
        return self.random_element(LESSON_TITLE)


class Command(BaseCommand):
    help = "Populate the database with some data"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        fake = Faker("tw_GH")
        fake.add_provider(Provider)

        user_list = []

        # Create three users
        for _ in range(5):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name}-{last_name}@gmail.com"

            user = User(
                first_name=first_name,
                username=first_name,
                last_name=last_name,
                country="Ghana",
                city="Accra",
                email=email,
                password="testing321",
                is_active=True,
            )

            user_list.append(user)

        User.objects.bulk_create(user_list)

        curriculum_list = []

        # Create a number of CURRICULUM_LIST
        for _ in range(len(CURRICULUM_LIST)):
            data = fake.unique.course_curriculum()
            curriculum = Curriculum(name=data)
            curriculum_list.append(curriculum)

        Curriculum.objects.bulk_create(curriculum_list)

        year_list = []

        # Create a number of school year
        for _ in range(len(YEAR_LIST)):
            data = fake.unique.year_list()
            year = Year(value=data)
            year_list.append(year)

        Year.objects.bulk_create(year_list)

        self.stdout.write(
            self.style.SUCCESS(
                f"Number of curriculum created: {len(curriculum_list)}, Number of school years created: {len(year_list)}."
            )
        )

        # Create 10 courses with three lessons each
        pay = ["Paid", "Free"]
        for _ in range(10):

            course = Course.objects.create(
                curriculum=Curriculum.objects.order_by("?").first(),
                year=Year.objects.order_by("?").first(),
                instructor=Profile.objects.order_by("?").first(),
                title=random.choice(COURSE_TITLE),
                description=fake.text(max_nb_chars=70),
                cover_image="http://localhost:8000/media/course_images/interior_sample_Ihb2hNb.jpg",
                price=(round(random.uniform(9.99, 99.99), 2)),
                pay=random.choice(pay),
                status="Approved",
                published_status=True,
            )

            for i in range(len(LESSON_TITLE)):
                Lesson.objects.create(course_id=course.id, title=LESSON_TITLE[i], description="I love what this it")
