from django.core.cache import cache
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import RedirectView, TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.views import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .filters import ShortenedUrlStatisticsFilter
from .models import ShortenedUrl, ShortenedUrlStatistics
from .permissions import IsOwner
from .serializers import ShortenedUrlSerializer, ShortenedUrlStatisticsSerializer


OPENAPI_REQUEST_EXAMPLE_VALUE = {
    "name": "google",
    "description": "google",
    "source_url": "https://google.com",
}

OPENAPI_RESPONSE_EXAMPLE_VALUE = {
    "id": 1,
    "name": "google",
    "description": "google",
    "prefix": "g",
    "source_url": "https://google.com",
    "target_url": "Exg89FF",
    "created_time": "2023-12-15T04:47:52.689Z",
    "updated_time": "2023-12-15T04:52:52.789Z",
}

OPENAPI_DEFAULT_EXAMPLES = [
    OpenApiExample(
        name="Example 1",
        value=OPENAPI_RESPONSE_EXAMPLE_VALUE,
    ),
]

OPENAPI_REQUEST_RESPONSE_EXAMPLES = [
    OpenApiExample(
        name="Example 1",
        value=OPENAPI_REQUEST_EXAMPLE_VALUE,
        request_only=True,
    ),
    OpenApiExample(
        name="Example 1",
        value=OPENAPI_RESPONSE_EXAMPLE_VALUE,
        response_only=True,
    ),
]


class ShortenedUrlViewSet(ModelViewSet):
    queryset = ShortenedUrl.objects.all()
    serializer_class = ShortenedUrlSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]

    @extend_schema(examples=OPENAPI_DEFAULT_EXAMPLES)
    def list(self, request, *args, **kwargs):
        queryset = ShortenedUrl.objects.filter(creator=request.user)
        serializer = ShortenedUrlSerializer(queryset, many=True)

        return Response(serializer.data)

    @extend_schema(examples=OPENAPI_REQUEST_RESPONSE_EXAMPLES)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(examples=OPENAPI_DEFAULT_EXAMPLES)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(examples=OPENAPI_REQUEST_RESPONSE_EXAMPLES)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(examples=OPENAPI_REQUEST_RESPONSE_EXAMPLES)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ShortenedUrlRedirectionView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        prefix = kwargs["prefix"]
        target_url = kwargs["target_url"]

        # Look Aside 방식으로 데이터를 가져옴
        # 기본 키 만료 시간 5분
        # 캐시 스템피드 문제 존재(TTL 만료 시간을 업데이트하여 개선할 수 있음)

        cached_shortened_url_id_and_source_url = cache.get(
            f"shortened_url:{prefix}:{target_url}"
        )

        if cached_shortened_url_id_and_source_url is None:
            shortened_url = get_object_or_404(
                ShortenedUrl, prefix=prefix, target_url=target_url
            )

            shortened_url_id = shortened_url.id
            shortened_url_source_url = shortened_url.source_url

            cache.set(
                f"shortened_url:{prefix}:{target_url}",
                {"id": shortened_url_id, "source_url": shortened_url_source_url},
            )
        else:
            shortened_url_id = cached_shortened_url_id_and_source_url["id"]
            shortened_url_source_url = cached_shortened_url_id_and_source_url[
                "source_url"
            ]

        try:
            with transaction.atomic():
                today = timezone.now().date()

                # 동시에 자원 접근 시 트랙잭션이 끝날 때까지 자원을 잠금
                shortened_url_statistics = (
                    ShortenedUrlStatistics.objects.select_for_update().get(
                        date=today, shortened_url=shortened_url_id
                    )
                )
                shortened_url_statistics.record()
        except ShortenedUrlStatistics.DoesNotExist:
            ShortenedUrlStatistics.objects.create(
                date=today, shortened_url=shortened_url, clicked=1
            )

        return shortened_url_source_url


class ShortenedUrlNewView(LoginRequiredMixin, TemplateView):
    template_name = "shortened_url/new.html"


class ShortenedUrlDetailView(LoginRequiredMixin, TemplateView):
    template_name = "shortened_url/detail.html"

    def get(self, request, *args, **kwargs):
        id = kwargs["pk"]
        user = request.user
        shortened_url = get_object_or_404(ShortenedUrl, pk=id, creator=user)

        return render(request, self.template_name)


class ShortenedUrlStatisticsView(ListAPIView):
    serializer_class = ShortenedUrlStatisticsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShortenedUrlStatisticsFilter

    def get_queryset(self):
        creator = self.request.user
        queryset = ShortenedUrlStatistics.objects.filter(shortened_url__creator=creator)

        return queryset
