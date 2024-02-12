from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ShortenedUrlViewSet, ShortenedUrlStatisticsView


router = DefaultRouter()
router.register(r"shortened-urls", ShortenedUrlViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "shortened-url-statistics/",
        ShortenedUrlStatisticsView.as_view(),
        name="shortened-url-statistics",
    ),
]
