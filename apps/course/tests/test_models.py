import pytest


def test_curriculum_str(course_curriculum):
    assert course_curriculum.__str__() == "GCSE"


def test_year_str(course_year):
    assert course_year.__str__() == 12


def test_course_str(course):
    assert course.__str__() == "Mathematics"


def test_course_lesson_str(course_lesson):
    assert course_lesson.__str__() == "Lesson One"
