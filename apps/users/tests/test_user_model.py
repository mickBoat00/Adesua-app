import pytest


def test_user_str(user):
    assert user.__str__() == "Miiickeys"
    assert user.get_full_name == "Mickeys - Boateng"


def test_user_str(adminuser):
    assert adminuser.__str__() == "admin_user"
