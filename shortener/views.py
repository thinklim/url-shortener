from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from .models import ShortenedUrl
from .permissions import IsOwner
from .serializers import ShortenedUrlSerializer


class ShortenedUrlViewSet(ModelViewSet):
    queryset = ShortenedUrl.objects.all()
    serializer_class = ShortenedUrlSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = ShortenedUrl.objects.filter(creator=request.user)
        serializer = ShortenedUrlSerializer(queryset, many=True)

        return Response(serializer.data)
