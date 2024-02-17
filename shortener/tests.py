import pytest

from datetime import timedelta
from django.core.cache import cache
from django.utils import timezone
from django.http import HttpResponseRedirect
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_302_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from accounts.models import CustomUser
from .models import ShortenedUrl, ShortenedUrlStatistics


EXAMPLE_URL = "https://example.com"


@pytest.fixture
def sample_password():
    return "sample_pw"


@pytest.fixture
def create_user(db, django_user_model, sample_password):
    def make_user(**kwargs):
        if "password" not in kwargs:
            kwargs["password"] = sample_password

        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_shortened_url():
    def make_shortened_url(**kwargs):
        if "name" not in kwargs:
            kwargs["name"] = "example"

        if "source_url" not in kwargs:
            kwargs["source_url"] = EXAMPLE_URL

        return ShortenedUrl.objects.create(**kwargs)

    return make_shortened_url


@pytest.fixture
def create_shortened_url_statistics():
    def make_shortened_url_statistics(**kwargs):
        return ShortenedUrlStatistics.objects.create(**kwargs)

    return make_shortened_url_statistics


@pytest.mark.django_db
def test_shortened_url():
    user1 = CustomUser.objects.create_user(
        email="sample@example.com", password="test_example"
    )
    user2 = CustomUser.objects.create_user(
        email="test@example.com", password="test_example"
    )

    shortened_url = ShortenedUrl.objects.create(
        name="example", creator=user1, source_url=EXAMPLE_URL
    )

    assert ShortenedUrl.objects.count() == 1
    assert shortened_url.name == "example"
    assert len(shortened_url.prefix) == 1
    assert len(shortened_url.target_url) == 7
    assert shortened_url.creator != user2

    shortened_url.name = "test"
    shortened_url.save()

    assert shortened_url.created_time < shortened_url.updated_time


@pytest.mark.django_db
def test_shortened_url_api(create_user, create_shortened_url, sample_password):
    LOCALHOST_API_ENDPOINT = "http://127.0.0.1:8000/api"

    user1 = create_user(email="sample@example.com")
    user2 = create_user(email="sample2@example.com")
    shortened_url1 = create_shortened_url(creator=user1)
    shortened_url2 = create_shortened_url(name="example2", creator=user1)
    shortened_url3 = create_shortened_url(creator=user2)

    # 인증 없이 접근
    client1 = APIClient()
    response = client1.get(f"{LOCALHOST_API_ENDPOINT}/shortened-urls/")

    assert response.status_code == HTTP_403_FORBIDDEN

    # 인증 후 접근
    client1.login(email=user1.email, password=sample_password)
    response = client1.get(f"{LOCALHOST_API_ENDPOINT}/shortened-urls/")

    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 2

    # 자신의 리소스가 아닌 것에 접근
    response = client1.get(
        f"{LOCALHOST_API_ENDPOINT}/shortened-urls/{shortened_url3.id}/"
    )

    assert response.status_code == HTTP_403_FORBIDDEN

    # 생성
    response = client1.post(
        f"{LOCALHOST_API_ENDPOINT}/shortened-urls/",
        {"name": "example2", "description": "", "source_url": EXAMPLE_URL},
        "json",
    )

    assert response.status_code == HTTP_201_CREATED

    # 전체 수정
    assert ShortenedUrl.objects.get(id=shortened_url1.id).name == "example"

    response = client1.put(
        f"{LOCALHOST_API_ENDPOINT}/shortened-urls/{shortened_url1.id}/",
        {"name": "test", "source_url": EXAMPLE_URL},
        "json",
    )

    assert response.status_code == HTTP_200_OK
    assert ShortenedUrl.objects.get(id=shortened_url1.id).name == "test"

    # 부분 수정
    assert ShortenedUrl.objects.get(id=shortened_url1.id).source_url == EXAMPLE_URL

    response = client1.patch(
        f"{LOCALHOST_API_ENDPOINT}/shortened-urls/{shortened_url1.id}/",
        {"source_url": "https://test.com"},
        "json",
    )

    assert response.status_code == HTTP_200_OK
    assert (
        ShortenedUrl.objects.get(id=shortened_url1.id).source_url == "https://test.com"
    )

    # 삭제
    response = client1.delete(
        f"{LOCALHOST_API_ENDPOINT}/shortened-urls/{shortened_url1.id}/"
    )

    assert response.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_shortened_url_redirection(
    create_user, create_shortened_url, create_shortened_url_statistics, sample_password
):
    user1 = create_user(email="sample@example.com")
    shortened_url = create_shortened_url(creator=user1)
    prefix = shortened_url.prefix
    target_url = shortened_url.target_url

    client1 = APIClient()
    client1.login(email=user1, password=sample_password)

    # 존재하는 단축 URL로 접근
    response = client1.get(f"/{prefix}/{target_url}/")

    assert response.status_code == HTTP_302_FOUND
    assert type(response) == HttpResponseRedirect
    assert response.url == EXAMPLE_URL

    today = timezone.now().date()
    shortened_url_statistics = ShortenedUrlStatistics.objects.get(
        date=today, shortened_url=shortened_url.id
    )
    assert shortened_url_statistics.clicked == 1

    response = client1.get(f"/{prefix}/{target_url}/")

    shortened_url_statistics = ShortenedUrlStatistics.objects.get(
        date=today, shortened_url=shortened_url.id
    )
    assert shortened_url_statistics.clicked == 2

    # 존재하지 않는 단축 URL로 접근
    response = client1.get(f"/xxx/wrong/")

    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_shortened_url_detail(create_user, create_shortened_url, sample_password):
    user1 = create_user(email="sample@example.com")
    user2 = create_user(email="sample2@example.com")
    shortened_url1 = create_shortened_url(creator=user1)
    shortened_url2 = create_shortened_url(creator=user2)

    client1 = APIClient()
    client1.login(email=user1, password=sample_password)

    # 자신의 단축 URL 상세 페이지로 접근
    response = client1.get(f"/shortened-urls/{shortened_url1.id}/")

    assert response.status_code == HTTP_200_OK

    # 다른 사용자의 단축 URL 상세 페이지로 접근
    response = client1.get(f"/shortened-urls/{shortened_url2.id}/")

    assert response.status_code == HTTP_404_NOT_FOUND

    # 익명 사용자가 단축 URL 상세 페이지로 접근
    anonymous_client = APIClient()

    response = anonymous_client.get(f"/shortened-urls/{shortened_url1.id}/")

    assert response.status_code == HTTP_302_FOUND


@pytest.mark.django_db
def test_shortened_url_statistics(
    create_user, create_shortened_url, create_shortened_url_statistics
):
    today = timezone.now().date()
    user1 = create_user(email="sample@example.com")
    shortened_url1 = create_shortened_url(creator=user1)
    shortened_url_statistics1 = create_shortened_url_statistics(
        date=today, shortened_url=shortened_url1
    )

    assert shortened_url_statistics1.clicked == 0

    shortened_url_statistics1.record()

    assert shortened_url_statistics1.clicked == 1


@pytest.mark.django_db
def test_shortened_url_statistics_api(
    create_user, create_shortened_url, create_shortened_url_statistics, sample_password
):
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    user1 = create_user(email="sample@example.com")
    shortened_url1 = create_shortened_url(creator=user1)

    user2 = create_user(email="sample2@example.com")
    shortened_url2 = create_shortened_url(creator=user2)
    shortened_url3 = create_shortened_url(creator=user2)

    # shortened_url1 데이터 생성
    create_shortened_url_statistics(date=today, shortened_url=shortened_url1)
    create_shortened_url_statistics(date=tomorrow, shortened_url=shortened_url1)

    # shortened_url2 데이터 생성
    create_shortened_url_statistics(
        date=yesterday, shortened_url=shortened_url2, clicked=10
    )
    create_shortened_url_statistics(
        date=today, shortened_url=shortened_url2, clicked=20
    )
    create_shortened_url_statistics(
        date=tomorrow, shortened_url=shortened_url2, clicked=50
    )

    # shortened_url3 데이터 생성
    create_shortened_url_statistics(date=today, shortened_url=shortened_url3, clicked=5)

    # 사용자 1번 테스트
    client1 = APIClient()
    client1.login(email=user1, password=sample_password)

    response = client1.get(f"/api/shortened-url-statistics/")

    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 2

    # 사용자 2번 테스트(자신의 데이터만 조회 및 필터링 포함)
    client2 = APIClient()
    client2.login(email=user2, password=sample_password)

    response = client2.get(f"/api/shortened-url-statistics/")

    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 4

    response = client2.get(f"/api/shortened-url-statistics/?start_date={today}")

    assert len(response.data) == 3

    response = client2.get(f"/api/shortened-url-statistics/?min_clicked=30")

    assert len(response.data) == 1

    response = client2.get(
        f"/api/shortened-url-statistics/?start_date={today}&shortened_url={shortened_url3.id}"
    )

    assert len(response.data) == 1


def test_cache():
    cache.set("hello", "world")
    data = cache.get("hello")

    assert data == "world"


@pytest.mark.django_db
def test_delete_shortened_url_redirection_cache_signal(
    create_user, create_shortened_url, sample_password
):
    user = create_user(email="sample@example.com")
    shortened_url = create_shortened_url(creator=user)
    prefix = shortened_url.prefix
    target_url = shortened_url.target_url

    client = APIClient()
    client.login(email=user.email, password=sample_password)

    # Test 1: 단축 URL 수정 요청 테스트(HTTP PUT 메서드 호출)
    # 단축 URL 리디렉션
    response = client.get(f"/{prefix}/{target_url}/")

    assert response.status_code == HTTP_302_FOUND

    cached_shortend_url = cache.get(f"shortened_url:{prefix}:{target_url}")

    assert cached_shortend_url["source_url"] == shortened_url.source_url

    # 단축 URL 수정
    response = client.put(
        f"/api/shortened-urls/{shortened_url.id}/",
        {"name": "sample", "source_url": "http://sample.com"},
    )

    assert response.status_code == HTTP_200_OK

    cached_shortend_url = cache.get(f"shortened_url:{prefix}:{target_url}")

    assert cached_shortend_url is None

    # Test 2: 단축 URL 수정 요청 테스트(HTTP PATCH 메서드 호출)
    # 단축 URL 리디렉션
    response = client.get(f"/{prefix}/{target_url}/")

    assert response.status_code == HTTP_302_FOUND

    cached_shortend_url = cache.get(f"shortened_url:{prefix}:{target_url}")

    assert cached_shortend_url["source_url"] == "http://sample.com"

    # 단축 URL 수정
    response = client.patch(
        f"/api/shortened-urls/{shortened_url.id}/",
        {"source_url": "http://example.com"},
    )

    assert response.status_code == HTTP_200_OK

    cached_shortend_url = cache.get(f"shortened_url:{prefix}:{target_url}")

    assert cached_shortend_url is None
