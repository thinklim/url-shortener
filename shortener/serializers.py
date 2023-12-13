from rest_framework import serializers
from .models import ShortenedUrl


class ShortenedUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedUrl
        exclude = [
            "creator",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        name = validated_data["name"]
        description = validated_data["description"]
        source_url = validated_data["source_url"]
        creator = request.user

        return ShortenedUrl.objects.create(
            name=name, description=description, source_url=source_url, creator=creator
        )

    def update(self, instance, validated_data):
        request = self.context.get("request")
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.source_url = validated_data.get("source_url", instance.source_url)
        instance.creator = request.user
        instance.save()

        return instance
