import pytest
from pytest_factoryboy import register

from tests.factories import CourseFactory, CurriculumFactory, LessonFactory, YearFactory

register(CurriculumFactory)
register(YearFactory)
register(CourseFactory)
register(LessonFactory)


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
