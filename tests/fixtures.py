import pytest
from pytest_factoryboy import register

from tests.factories import (  # CourseInstructorFactory,
    CourseFactory,
    CurriculumFactory,
    FirstInstructorFactory,
    LessonFactory,
    StudentUserFactory,
    UserInstructorFactory,
    YearFactory,
)

register(CurriculumFactory)
register(YearFactory)
register(CourseFactory)
register(LessonFactory)
register(FirstInstructorFactory)
register(UserInstructorFactory)
register(StudentUserFactory)


@pytest.fixture
def course_curriculum(db, curriculum_factory):
    curriculum = curriculum_factory.create()
    return curriculum


@pytest.fixture
def course_year(db, year_factory):
    year = year_factory.create()
    return year


@pytest.fixture
def course(db, course_factory):
    course = course_factory.create()
    return course


@pytest.fixture
def course_lesson(db, lesson_factory):
    lesson = lesson_factory.create()
    return lesson


@pytest.fixture
def firstinstructor(db, first_instructor_factory):
    new_user = first_instructor_factory.create()
    return new_user


# @pytest.fixture
# def course_instructor(db, course_instructor_factory):
#     instructor = course_instructor_factory.create()
#     return instructor


@pytest.fixture
def adminuser(db, user_factory):
    new_user = user_factory.create(username="admin_user", is_staff=True, is_superuser=True)
    return new_user


@pytest.fixture
def secondinstructor(db, user_instructor_factory):
    new_user = user_instructor_factory.create()
    return new_user


@pytest.fixture
def studentuser(db, student_user_factory):
    new_user = student_user_factory.create()
    return new_user


@pytest.fixture
def coursedata(db, student_user_factory):
    return {
        "curriculum": course_curriculum,
        "year": course_year,
        "title": "Science",
        "description": "fake.paragraph(nb_sentences=5)",
        "price": "10.99",
        "pay": "Paid",
        "published_status": True,
    }
