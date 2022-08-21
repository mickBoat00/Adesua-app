import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_view_courses(client):
    """
    Test all users can view courses list
    """

    url = reverse("course:course-list")
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK


# def test_view_a_course(db, client):

#     """
#     Test all users view a particular course's detail.
#     """

#     url = reverse("course:course-detail", kwargs={"slug": self.test_course.slug})
#     response = client.get(url, format="json")
#     assert response.status_code == status.HTTP_200_OK
