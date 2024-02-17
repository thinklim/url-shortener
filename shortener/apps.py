from django.apps import AppConfig


class ShortenerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shortener"

    def ready(self) -> None:
        # 암시적으로 receiver() 데코레이터가 선언된 메서드를 연결
        from . import signals
