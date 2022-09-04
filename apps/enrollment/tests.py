import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_student_enrollment(course, studentuser):
    url = reverse("student:course-enrollment")
    client.force_authenticate(user=studentuser)
    response = client.post(url, data={"course": str(course.id), "price": "10.99"}, format="json")
    assert response.status_code == status.HTTP_201_CREATED


