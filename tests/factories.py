import factory
from apps.course.models import Course, Curriculum, Lesson, Year
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()

User = get_user_model()

from apps.users.models import CourseInstructor, CustomUserManager, User


class CurriculumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Curriculum

    name = "GCSE"


class YearFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Year

    value = 12


class FirstInstructorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = "Mickeys"
    last_name = "Boateng"
    username = "Miiickeys"
    email = "mikeboateng17@gmail.com"
    type = "INSTRUCTOR"
    password = "testing321"
    is_active = True
    is_staff = False


class UserInstructorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = "ui"
    last_name = "iod"
    username = "io"
    email = "iouid@gmail.com"
    type = "INSTRUCTOR"
    password = "testing321"
    is_active = True
    is_staff = False


class StudentUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = "s"
    last_name = "s"
    username = "s"
    email = "student@gmail.com"
    type = "STUDENT"
    password = "testing321"
    is_active = True
    is_staff = False


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    curriculum = factory.SubFactory(CurriculumFactory)
    year = factory.SubFactory(YearFactory)
    instructor = factory.SubFactory(FirstInstructorFactory)
    title = "Mathematics"
    slug = "mathematics"
    description = "Mathematics for Year 12"
    cover_image = "http://localhost:8000/media/course_images/interior_sample_Ihb2hNb.jpg"
    price = 10.99
    pay = "Free"
    status = "Approved"
    published_status = True


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lesson

    course = factory.SubFactory(CourseFactory)
    title = "Lesson One"
    slug = "lesson-one"
    description = "This is the first Lesson for the course Mathematics for Year 12"
    video = "http://localhost:8000/media//lesson_videos/videoplayback_1.mp4"


"""
Users app Factory
"""
