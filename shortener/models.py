import string
import random

from django.db import models
from django.conf import settings


class ShortenedUrl(models.Model):
    def get_random_letter():
        letters = string.ascii_lowercase

        return random.choice(letters)

    def get_random_string():
        letters = f"{string.digits}{string.ascii_letters}"

        return "".join([random.choice(letters) for _ in range(7)])

    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500, blank=True, default="")
    prefix = models.CharField(max_length=50, default=get_random_letter)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    source_url = models.URLField(max_length=1000)
    target_url = models.CharField(max_length=7, default=get_random_string)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "shortened_url"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["prefix"]),
            models.Index(fields=["source_url"]),
            models.Index(fields=["target_url"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["prefix", "target_url"], name="unique_shortened_url"
            )
        ]

    def __str__(self) -> str:
        return self.name
