from django.test import TestCase
from .models import Course, Lesson
from apps.profiles.models import Profile

from django.contrib.auth import get_user_model
User = get_user_model()


"""
    1. test user 2 create lesson for course user 1 created
"""


class Test_Create_Course(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_course = Course.objects.create(
            instructor_id = 1,
            title = "intro to django",
            description = "This is an introduction to django",
            price = "10.99",
            pay = "Free",
            published_status = True,
        )

        testuser1 = User.objects.create_user(
            username = "Test", 
            first_name = "Test", 
            last_name = "User", 
            email = "test.user@gmail.com", 
            password = "pass1234567", 
        )

        testuser2 = User.objects.create_user(
            username = "Test 1", 
            first_name = "Test 1", 
            last_name = "Me", 
            email = "test1_user@gmail.com", 
            password = "pass1234567", 
        )

        lesson1 = Lesson.objects.create(
            course = test_course,
            title = 'Lesson One', 
            description= 'I love what this it'
        )

    # def test_profile_creation_signal(self):
    #     user = User.objects.get(id=1)
    #     profile = Profile.objects.get(id=1)
    #     print('profile', profile)
    #     self.assertEqual(user, profile.user)

    def test_free_course_price(self):
        course = Course.objects.get(id=1)



    def test_course_content(self):
        course = Course.objects.get(id=1)
        instructor = f'{course.instructor}'
        self.assertEqual(0.00, course.price)
        self.assertEqual(instructor, "Test's profile")
        self.assertEqual(str(course), "Intro To Django")

        
    def test_lesson_details(self):
        lesson = Lesson.objects.get(id=1)
        self.assertEqual(str(lesson), "Lesson One")
        self.assertEqual(str(lesson.slug), "lesson-one")


    def test_lesson_instructor(self):
        lesson = Lesson.objects.get(id=1)
        lesson_instructor = lesson.course.instructor
        self.assertNotEqual(str(lesson_instructor), "Test 1's profile")
        self.assertEqual(str(lesson), "Lesson One")



