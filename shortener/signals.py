from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShortenedUrl


@receiver(post_save, sender=ShortenedUrl)
def delete_shortened_url_redirection_cache(sender, instance, created, **kwargs):
    if not created:
        prefix = instance.prefix
        target_url = instance.target_url

        # Cache Invalidation
        cache.delete(f"shortened_url:{prefix}:{target_url}")
