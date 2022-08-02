from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.course.models import Course, Lesson, Student
from apps.profiles.models import Profile

User = get_user_model()


"""
    
    1. test user 2 create lesson for course user 1 created  def test_lesson_instructor(self)
    2. create an order and it should add self.request.user in students list?.

    Will a student table (student, course) enrolled be better then manytomanyfield in student
"""


class Test_Create_Course(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = User.objects.create_user(
            username="Test",
            first_name="Test",
            last_name="User",
            email="test.user@gmail.com",
            password="pass1234567",
        )

        test_course = Course.objects.create(
            instructor_id=1,
            title="intro to django",
            description="This is an introduction to django",
            price="10.99",
            pay="Free",
            published_status=True,
        )

        testuser2 = User.objects.create_user(
            username="Test 1",
            first_name="Test 1",
            last_name="Me",
            email="test1_user@gmail.com",
            password="pass1234567",
        )

        lesson1 = Lesson.objects.create(course=test_course, title="Lesson One", description="I love what this it")

    def test_profile_creation_signal(self):
        profile = Profile.objects.all()
        self.assertTrue(profile.exists())

    def test_course_content(self):
        course = Course.objects.get(id=1)
        instructor = f"{course.instructor}"
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

    """
        Student model added so error.
    """

    def test_student_course_enrollment(self):
        course = Course.objects.get(id=1)
        user = Profile.objects.get(id=2)

        Student.objects.create(course=course, profile=user)

        self.assertEqual(course.students.count(), 1)


class CourseTests(APITestCase):
    def test_student_course_enrollment(self):

        """
        Test a situation where a user access lessons of course, he is enrolled in.
        """

        testuser1 = User.objects.create_user(
            username="Test",
            first_name="Test",
            last_name="User",
            email="test.user@gmail.com",
            password="pass1234567",
        )

        client = APIClient()
        client.login(email="test.user@gmail.com", password="pass1234567")

        data = {
            "title": "intro to django",
            "description": "This is an introduction to django",
            "price": "10.99",
            "pay": "Free",
        }

        url = reverse("course-create")
        client.post(url, data, format="json")
        client.logout()

        testuser2 = User.objects.create_user(
            username="Test 2",
            first_name="Test 2",
            last_name="User two",
            email="test.user_two@gmail.com",
            password="pass1234567",
        )

        print("cccc", Course.objects.all().values("id"))

        client.login(email="test.user_two@gmail.com", password="pass1234567")

        data = {"course": 3, "price": 9.99}

        url = reverse("pay-course")
        response = client.post(url, data, format="json")

        url = reverse("course-lesson", kwargs={"slug": "intro-to-django"})
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_course_lessons_access(self):

        """
        Test a situation where a user can't access a lessons of course, he is not enrolled in.
        """

        testuser1 = User.objects.create_user(
            username="Test",
            first_name="Test",
            last_name="User",
            email="test.user@gmail.com",
            password="pass1234567",
        )

        client = APIClient()
        client.login(email="test.user@gmail.com", password="pass1234567")

        data = {
            "title": "intro to django",
            "description": "This is an introduction to django",
            "price": "10.99",
            "pay": "Free",
        }

        url = reverse("course-create")
        client.post(url, data, format="json")
        client.logout()

        testuser2 = User.objects.create_user(
            username="Test 2",
            first_name="Test 2",
            last_name="User two",
            email="test.user_two@gmail.com",
            password="pass1234567",
        )

        client.login(email="test.user_two@gmail.com", password="pass1234567")

        url = reverse("course-lesson", kwargs={"slug": "intro-to-django"})
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course(self):

        """
        Test a situation where user1 create a course and user2 is trying to update that course
        Expected result is user2 should be Forbidden from updating course he didn't create
        """

        testuser1 = User.objects.create_user(
            username="Test",
            first_name="Test",
            last_name="User",
            email="test.user@gmail.com",
            password="pass1234567",
        )

        client = APIClient()
        client.login(email="test.user@gmail.com", password="pass1234567")

        data = {
            "title": "intro to django",
            "description": "This is an introduction to django",
            "price": "10.99",
            "pay": "Free",
        }

        url = reverse("course-create")
        client.post(url, data, format="json")
        client.logout()

        testuser2 = User.objects.create_user(
            username="Test 2",
            first_name="Test 2",
            last_name="User two",
            email="test.user_two@gmail.com",
            password="pass1234567",
        )

        client.login(email="test.user_two@gmail.com", password="pass1234567")

        update_course = {"price": "9.99", "pay": "Paid", "published_status": "True"}

        url = reverse("course-detail", kwargs={"slug": "intro-to-django"})
        response = client.patch(url, update_course, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course_lesson(self):

        """
        Test a situation where user1 create a course and user2 is trying to create a lesson for that course
        Expected result is user2 should be Forbidden from creating a lesson for a course he didn't create
        """

        testuser1 = User.objects.create_user(
            username="Test",
            first_name="Test",
            last_name="User",
            email="test.user@gmail.com",
            password="pass1234567",
        )

        client = APIClient()
        client.login(email="test.user@gmail.com", password="pass1234567")

        data = {
            "title": "intro to django",
            "description": "This is an introduction to django",
            "price": "10.99",
            "pay": "Free",
            "published_status": True,
        }

        url = reverse("course-create")
        client.post(url, data, format="json")
        client.logout()

        testuser2 = User.objects.create_user(
            username="Test 2",
            first_name="Test 2",
            last_name="User two",
            email="test.user_two@gmail.com",
            password="pass1234567",
        )

        client.login(email="test.user_two@gmail.com", password="pass1234567")

        lesson_data = {"course": 1, "title": "Lesson One", "description": "Love this course"}

        url = reverse("lesson-create")
        response = client.post(url, lesson_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_courses(self):

        """
        An authenticated user should be able to create a course
        """

        testuser1 = User.objects.create_user(
            username="Test",
            first_name="Test",
            last_name="User",
            email="test.user@gmail.com",
            password="pass1234567",
        )

        client = APIClient()
        client.login(email="test.user@gmail.com", password="pass1234567")

        data = {
            "title": "intro to noo",
            "description": "This is an introduction to django",
            "price": "10.99",
            "pay": "Free",
            "published_status": True,
        }

        url = reverse("course-create")
        response = client.post(url, data, format="json")

        # print('COurse', Course.objects.all().first().instructor)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_a_course(self):

        """
        Test view a particular course created.
        """

        testuser1 = User.objects.create_user(
            username="Test",
            first_name="Test",
            last_name="User",
            email="test.user@gmail.com",
            password="pass1234567",
        )

        test_course = Course.objects.create(
            instructor_id=10,
            title="intro to django",
            description="This is an introduction to django",
            price="10.99",
            pay="Free",
            published_status=True,
        )

        url = reverse("course-detail", kwargs={"slug": "intro-to-django"})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_courses(self):
        """
        Test to view all courses created.
        """

        url = reverse("course-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
