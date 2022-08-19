from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.course.models import Course, Curriculum, Year

User = get_user_model()

from faker import Faker

fake = Faker()

import pytest


def test_demo(test_fixture1):
    print("function_fixture")
    assert test_fixture1 == 1


# class CourseTests(APITestCase):
#     def test_demo(test_fixture1):
#         print("function_fixture")
#         assert test_fixture1 == 1

# def setUp(self):

#     self.course_instructor = User.objects.create_user(
#         first_name=fake.first_name(),
#         last_name=fake.last_name(),
#         username=fake.user_name(),
#         type="INSTRUCTOR",
#         email=fake.email(),
#         password="pass1234567",
#     )

#     self.course_instructor2 = User.objects.create_user(
#         first_name=fake.first_name(),
#         last_name=fake.last_name(),
#         username=fake.user_name(),
#         type="INSTRUCTOR",
#         email=fake.email(),
#         password="pass1234567",
#     )

#     self.student = User.objects.create_user(
#         first_name=fake.first_name(),
#         last_name=fake.last_name(),
#         username=fake.user_name(),
#         type="STUDENT",
#         email=fake.email(),
#         password="pass1234567",
#     )

#     self.test_curriculum = Curriculum.objects.create(name="GCSE")

#     self.test_year = Year.objects.create(value=10)

#     self.test_course = Course.objects.create(
#         curriculum=self.test_curriculum,
#         year=self.test_year,
#         instructor=self.course_instructor,
#         title="Mathematics",
#         description=fake.paragraph(nb_sentences=5),
#         price="10.99",
#         pay="Free",
#         published_status=True,
#         status="Approved",
#     )

#     self.create_course_data = {
#         "curriculum": self.test_curriculum.id,
#         "year": self.test_year.id,
#         "title": "Science",
#         "description": fake.paragraph(nb_sentences=5),
#         "price": "10.99",
#         "pay": "Paid",
#         "published_status": True,
#     }

#     self.lesson_data = {
#         "title": "Lesson One",
#         "slug": "lesson-one",
#         "description": "Love this course",
#         "video": "http://localhost:8000/media/lesson_videos/videoplayback_1.mp4",
#     }

#     self.update_course = {"price": "9.99", "pay": "Paid", "published_status": "True"}

#     self.client = APIClient()

# def test_view_courses(self, test_fixture1):
#     """
#     Test all users can view courses list
#     """

#     url = reverse("course-list")
#     response = self.client.get(url, format="json")
#     self.assertEqual(response.status_code, status.HTTP_200_OK)

# def test_view_a_course(self):

#     """
#     Test all users view a particular course's detail.
#     """

#     url = reverse("course-detail", kwargs={"slug": self.test_course.slug})
#     response = self.client.get(url, format="json")
#     self.assertEqual(response.status_code, status.HTTP_200_OK)

# def test_create_courses(self):

#     """
#     Test if an unauthenticated user can create course
#     Test if students can create course
#     Test if only course instructors can create course
#     """

#     url = reverse("course-create")
#     response = self.client.post(url, self.create_course_data, format="json")

#     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     self.client.login(email=self.student.email, password="pass1234567")

#     url = reverse("course-create")
#     response = self.client.post(url, self.create_course_data, format="json")

#     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     self.client.logout()
#     self.client.login(email=self.course_instructor.email, password="pass1234567")

#     url = reverse("course-create")
#     response = self.client.post(url, self.create_course_data, format="json")

#     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# def test_create_course_lesson(self):

#     """
#     Test a situation where a course instructor creates a course and a different course instructor is trying
#     to create a lesson for that course
#     """

#     self.client.login(email=self.course_instructor2.email, password="pass1234567")

#     url = reverse("course-lesson", kwargs={"slug": self.test_course.slug})
#     response = self.client.post(url, self.lesson_data, format="json")
#     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# def test_student_course_lessons_access(self):

#     """
#     Test a situation where a student can't access a lessons of course, he/she is not enrolled in.
#     """

#     self.client.login(email=self.student.email, password="pass1234567")

#     url = reverse("course-lesson", kwargs={"slug": self.test_course.slug})
#     response = self.client.get(url, format="json")
#     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# def test_update_course(self):

#     """
#     Test a situation where only the course instructor for a course can update details of that particular course
#     Everyone else should be prevented. Except a reviewer who can only update the status of the course.
#     """

#     self.client.login(email=self.course_instructor2.email, password="pass1234567")

#     url = reverse("course-detail", kwargs={"slug": self.test_course.slug})
#     response = self.client.patch(url, self.update_course, format="json")
#     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     self.client.logout()

#     self.client.login(email=self.course_instructor.email, password="pass1234567")
#     url = reverse("course-detail", kwargs={"slug": self.test_course.slug})
#     response = self.client.patch(url, self.update_course, format="json")
#     self.assertEqual(response.status_code, status.HTTP_200_OK)
