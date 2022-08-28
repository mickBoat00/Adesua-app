# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient, APITestCase

# from apps.course.models import Course, Curriculum, Year

# User = get_user_model()


# """

#     1. test user 2 create lesson for course user 1 created  def test_lesson_instructor(self)
#     2. create an order and it should add self.request.user in students list?.

#     Will a student table (student, course) enrolled be better then manytomanyfield in student
# """


# class ReviewersTest(APITestCase):
#     def setUp(self):

#         self.course_instructor = User.objects.create_user(
#             first_name="Course",
#             last_name="Instructor",
#             username="course_instructor",
#             type="INSTRUCTOR",
#             email="course.instructor@gmail.com",
#             password="pass1234567",
#         )

#         self.course_instructor2 = User.objects.create_user(
#             first_name="Course 2",
#             last_name="Instructor 2",
#             username="course_instructor2",
#             type="INSTRUCTOR",
#             email="course.instructor_2@gmail.com",
#             password="pass1234567",
#         )

#         self.student = User.objects.create_user(
#             first_name="Student",
#             last_name="School",
#             username="student_school",
#             type="STUDENT",
#             email="student@gmail.com",
#             password="pass1234567",
#         )

#         self.reviewer = User.objects.create_user(
#             first_name="Re",
#             last_name="Viewer",
#             username="re_viewer",
#             type="REVIEWER",
#             email="re_viewer@gmail.com",
#             password="pass1234567",
#         )

#         self.test_curriculum = Curriculum.objects.create(name="GCSE")

#         self.test_year = Year.objects.create(value=10)

#         self.test_course = Course.objects.create(
#             curriculum=self.test_curriculum,
#             year=self.test_year,
#             instructor=self.course_instructor,
#             title="Mathematics",
#             description="This is a GCSE mathematice course for GCSE students.",
#             price="10.99",
#             pay="Free",
#             published_status=True,
#         )

#         self.client = APIClient()

#     def test_reviewers_update_pending_courses(self):

#         """
#         Reviewers should get a list of pending courses and update their status to approved..
#         """

#         self.client.login(email=self.reviewer.email, password="pass1234567")

#         # url = reverse("course-lesson", kwargs={"slug": "mathematics"})
#         # response = self.client.get(url, format="json")
#         # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#         # data = {"course": self.test_course.id, "price": 10.99}

#         # url = reverse("student:course-enrollment")
#         # response = self.client.post(url, data, format="json")

#         # url = reverse("course-lesson", kwargs={"slug": "mathematics"})
#         # response = self.client.get(url, format="json")
#         # self.assertEqual(response.status_code, status.HTTP_200_OK)
