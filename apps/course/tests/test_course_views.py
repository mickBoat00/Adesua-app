import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_view_courses():
    """
    Test all users can view courses list
    """

    url = reverse("course:courses-list")
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK


def test_view_a_course(db, course):

    """
    Test all users view a particular course's detail.
    """

    url = reverse("course:courses-detail", kwargs={"slug": course.slug})
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK


def test_create_courses(db, course_curriculum, course_year, studentuser, firstinstructor, coursedata):

    """
    Test if an unauthenticated user can create course
    Test if students can create course
    Test if only course instructors can create course
    """

    url = reverse("course:courses-list")
    response = client.post(
        url,
        data=coursedata,
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # A student user logins in
    client.force_authenticate(user=studentuser)

    response = client.post(
        url,
        data=coursedata,
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # A course instructor logins in
    client.force_authenticate(user=firstinstructor)

    response = client.post(
        url,
        data={
            "curriculum": course_curriculum.id,
            "year": course_year.id,
            "title": "Science",
            "description": "fake.paragraph(nb_sentences=5)",
            "price": "10.99",
            "pay": "Paid",
            "published_status": True,
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_course_lesson(db, course, secondinstructor):

    """
    Test a situation where a course instructor creates a course and a different course instructor is trying
    to create a lesson for that course
    """

    # A different instructor logs in to create lessons for courses he did not create.
    client.force_authenticate(user=secondinstructor)

    url = reverse("course:lessons-list", kwargs={"courseslug": course.slug})
    response = client.post(
        url,
        data={
            "title": "Lesson two",
            "slug": "lesson-two",
            "description": "Love this course",
            "video": "http://localhost:8000/media/lesson_videos/videoplayback_1.mp4",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_course(db, secondinstructor, course):

    """
    Test a situation where only the course instructor for a course can update details of that particular course
    Everyone else should be prevented. Except a reviewer who can only update the status of the course.
    """

    client.force_authenticate(user=secondinstructor)

    url = reverse("course:courses-detail", kwargs={"slug": course.slug})
    response = client.patch(url, data={"price": "9.99", "pay": "Paid", "published_status": "True"}, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # client.force_authenticate(user=None)

    # client.force_authenticate(user=user)
    # url = reverse("course:course-detail", kwargs={"slug": course.slug})
    # response = client.patch(url, data={"price": "9.99", "pay": "Paid", "published_status": "True"}, format="json")
    # assert response.status_code == status.HTTP_200_OK


def test_student_course_lessons_access(db, studentuser, course):

    """
    Test a situation where a student can't access a lessons of course, he/she is not enrolled in.
    """

    client.force_authenticate(user=studentuser)

    url = reverse("course:lessons-list", kwargs={"courseslug": course.slug})
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # enrollment_url = reverse("student:course-enrollment")
    # response = client.post(
    #     enrollment_url, data={"course": course, "student": studentuser, "price": 10.99}, format="json"
    # )
    # assert response.status_code == status.HTTP_403_FORBIDDEN
