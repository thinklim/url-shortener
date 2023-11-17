import pytest

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@pytest.mark.django_db
def test_user_create():
    email = "test@example.com"
    password = "test_example"

    CustomUser.objects.create_user(email, password)

    assert CustomUser.objects.count() == 1


@pytest.mark.django_db
def test_user_creation_form():
    form = CustomUserCreationForm(
        data={
            "email": "test@example.com",
            "password1": "test_example",
            "password2": "test_example",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_usr_change_form():
    form = CustomUserChangeForm(data={"password": "test_exam"})

    assert form.is_valid()
