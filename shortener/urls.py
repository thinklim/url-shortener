from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ShortenedUrlViewSet


router = DefaultRouter()
router.register(r"shortened-urls", ShortenedUrlViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
