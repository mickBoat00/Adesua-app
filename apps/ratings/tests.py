import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_course_rating(course):
    """
    Can we see the ratings of a course without logging in.
    """
    url = reverse("ratings:course-rating-list", kwargs={"courseslug": course.slug})
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_course_rating(course, studentuser):
    """
    Test a situation where a student has to be enrolled in a course before they can rate it.
    """

    course_rating_url = reverse("ratings:course-rating-list", kwargs={"courseslug": course.slug})
    enrollment_url = reverse("student:course-enrollment")

    # Sign In student
    client.force_authenticate(user=studentuser)

    # Student should not be a able to rate a course before they are enrolled
    response = client.post(course_rating_url, data={"rating": "1", "comment": "I loved this course"}, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Student has to enroll in the course
    response = client.post(enrollment_url, data={"course": str(course.id), "price": "10.99"}, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    # After enrollment student, can now rate the course ?
    response = client.post(course_rating_url, data={"rating": "1", "comment": "I loved this course"}, format="json")

    assert response.status_code == status.HTTP_201_CREATED
