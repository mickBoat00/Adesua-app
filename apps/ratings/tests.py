from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.course.models import Course, Curriculum, Lesson, Student, Year
from apps.profiles.models import Profile

User = get_user_model()


"""
    
    1. test user 2 create lesson for course user 1 created  def test_lesson_instructor(self)
    2. create an order and it should add self.request.user in students list?.

    Will a student table (student, course) enrolled be better then manytomanyfield in student
"""


class RatingsTest(APITestCase):
    def setUp(self):

        self.course_instructor = User.objects.create_user(
            first_name="Course",
            last_name="Instructor",
            username="course_instructor",
            type="INSTRUCTOR",
            email="course.instructor@gmail.com",
            password="pass1234567",
        )

        self.course_instructor2 = User.objects.create_user(
            first_name="Course 2",
            last_name="Instructor 2",
            username="course_instructor2",
            type="INSTRUCTOR",
            email="course.instructor_2@gmail.com",
            password="pass1234567",
        )

        self.student = User.objects.create_user(
            first_name="Student",
            last_name="School",
            username="student_school",
            type="STUDENT",
            email="student@gmail.com",
            password="pass1234567",
        )

        self.test_curriculum = Curriculum.objects.create(name="GCSE")

        self.test_year = Year.objects.create(value=10)

        self.test_course = Course.objects.create(
            curriculum=self.test_curriculum,
            year=self.test_year,
            instructor=self.course_instructor,
            title="Mathematics",
            description="This is a GCSE mathematice course for GCSE students.",
            price="10.99",
            pay="Free",
            published_status=True,
            status="Approved",
        )

        self.client = APIClient()

    def test_student_rate_course(self):

        """
        Test enrolled students of a course should be able to able to rate that course
        Students not enrolled in the course should not be able to rate the course.
        """

        self.client.login(email="student@gmail.com", password="pass1234567")

        data = {"course": self.test_course.id, "rating": 4, "comment": "This is an amazing course."}

        rating_url = reverse("ratings:rate-course")

        response = self.client.post(rating_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        data = {"course": self.test_course.id, "price": 10.99}

        enrollment_url = reverse("student:course-enrollment")
        response = self.client.post(enrollment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(rating_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
