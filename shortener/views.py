from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from .models import ShortenedUrl
from .permissions import IsOwner
from .serializers import ShortenedUrlSerializer


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
