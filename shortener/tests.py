import pytest

from accounts.models import CustomUser
from .models import ShortenedUrl


@pytest.mark.django_db
def test_shortener_url():
    user1 = CustomUser.objects.create_user(
        email="sample@example.com", password="test_example"
    )
    user2 = CustomUser.objects.create_user(
        email="test@example.com", password="test_example"
    )

    shortened_url = ShortenedUrl.objects.create(
        name="example", creator=user1, source_url="https://example.com"
    )

    assert ShortenedUrl.objects.count() == 1
    assert shortened_url.name == "example"
    assert len(shortened_url.prefix) == 1
    assert len(shortened_url.target_url) == 7
    assert shortened_url.creator != user2

    shortened_url.name = "test"
    shortened_url.save()

    assert shortened_url.created_time < shortened_url.updated_time
