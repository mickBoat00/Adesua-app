import pytest


def test_user_str(db, firstinstructor):
    assert firstinstructor.__str__() == "Miiickeys"
    assert firstinstructor.get_full_name == "Mickeys - Boateng"


def test_user_str(db, adminuser):
    assert adminuser.__str__() == "admin_user"
