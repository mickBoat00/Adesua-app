import pytest


@pytest.fixture(scope="session")
def test_fixture1():
    print("Run each test")
    return 1
