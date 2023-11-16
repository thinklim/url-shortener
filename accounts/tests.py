import pytest

from .models import CustomUser


@pytest.mark.django_db
def test_user_create():
    email = "test@example.com"
    password = "test_example"

    CustomUser.objects.create_user(email, password)

    assert CustomUser.objects.count() == 1
