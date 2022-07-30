from django.test import TestCase
from apps.profiles.models import Profile

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.course.models import Course, Lesson

from django.contrib.auth import get_user_model
User = get_user_model()


"""
    
    1. test user 2 create lesson for course user 1 created  def test_lesson_instructor(self)
    2. create an order and it should add self.request.user in students list?.

    Will a student table (student, course) enrolled be better then manytomanyfield in student
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

    def test_profile_creation_signal(self):
        profile = Profile.objects.get(id=1)
        self.assertTrue(profile)

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


    def test_student_course_enrollment(self):
        course = Course.objects.get(id=1)
        student = Profile.objects.get(id=2)
        course.students.add(student)
        self.assertEqual(course.students.count(), 1)



class CourseTests(APITestCase):
    def test_view_course(self):
        url = reverse('course-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

    def test_create_course(self):

        client = APIClient()
        self.testuser1 = User.objects.create_user(
            username = "Test", 
            first_name = "Test", 
            last_name = "User", 
            email = "test.user@gmail.com", 
            password = "pass1234567", 
        )

        self.test_profile = Profile.objects.create(user=self.testuser1)

        data = {
            "instructor": 1,
            "title": "intro to django",
            "description": "This is an introduction to django",
            "price": "10.99",
            "pay": "Free",
            "published_status": True,
        }

        client.login(email="test.user@gmail.com", password = "pass1234567")

        url = reverse('course-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
