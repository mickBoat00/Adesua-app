from apps.course.models import Course, Curriculum, Lesson, Student, Year
from apps.profiles.models import Profile
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


"""
    
    1. test user 2 create lesson for course user 1 created  def test_lesson_instructor(self)
    2. create an order and it should add self.request.user in students list?.

    Will a student table (student, course) enrolled be better then manytomanyfield in student
"""


class CourseTests(APITestCase):
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

    def test_view_courses(self):
        """
        Test all users can view courses list
        """

        url = reverse("course-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_a_course(self):

        """
        Test all users view a particular course's detail.
        """

        url = reverse("course-detail", kwargs={"slug": "mathematics"})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_courses(self):

        """
        Test if an unauthenticated user can create course
        Test if students can create course
        Test if only course instructors can create course
        """

        data = {
            "curriculum": self.test_curriculum.id,
            "year": self.test_year.id,
            "title": "Science",
            "description": "This is a science ccourse for GCSE",
            "price": "10.99",
            "pay": "Free",
            "published_status": True,
        }

        url = reverse("course-create")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(email="student@gmail.com", password="pass1234567")

        url = reverse("course-create")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()
        self.client.login(email="course.instructor@gmail.com", password="pass1234567")

        url = reverse("course-create")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_lesson(self):

        """
        Test a situation where a course instructor creates a course and a different course instructor is trying
        to create a lesson for that course
        """

        self.client.login(email="course.instructor_2@gmail.com", password="pass1234567")

        lesson_data = {
            "title": "Lesson One",
            "slug": "lesson-one",
            "description": "Love this course",
            "video": "http://localhost:8000/media/lesson_videos/videoplayback_1.mp4",
        }

        url = reverse("course-lesson", kwargs={"slug": "mathematics"})
        response = self.client.post(url, lesson_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_course_lessons_access(self):

        """
        Test a situation where a student can't access a lessons of course, he/she is not enrolled in.
        """

        self.client.login(email="student@gmail.com", password="pass1234567")

        url = reverse("course-lesson", kwargs={"slug": "mathematics"})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course(self):

        """
        Test a situation where only the course instructor for a course can update details of that particular course
        Everyone else should be prevented. Except a reviewer who can only update the status of the course.
        """

        self.client.login(email="course.instructor_2@gmail.com", password="pass1234567")

        update_course = {"price": "9.99", "pay": "Paid", "published_status": "True"}

        url = reverse("course-detail", kwargs={"slug": "mathematics"})
        response = self.client.patch(url, update_course, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

        self.client.login(email="course.instructor@gmail.com", password="pass1234567")
        url = reverse("course-detail", kwargs={"slug": "mathematics"})
        response = self.client.patch(url, update_course, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
