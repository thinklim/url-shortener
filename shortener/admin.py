from datetime import datetime
from django.contrib import admin
from .models import ShortenedUrl


CUSTOM_DATETIME_FORMAT_WITH_TIMEZON = "%Y-%m-%d %H:%M:%S%z"


class ShortenedUrlAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "source_url",
        "prefix",
        "target_url",
        "creator",
        "view_created_time",
        "view_updated_time",
    ]
    list_filter = [
        "creator",
    ]
    search_fields = [
        "name",
        "creator__email",
    ]
    search_help_text = "이름과 사용자의 이메일 주소로 검색할 수 있습니다."

    @admin.display(description="created time")
    def view_created_time(self, obj):
        return datetime.strftime(obj.created_time, CUSTOM_DATETIME_FORMAT_WITH_TIMEZON)

    @admin.display(description="updated time")
    def view_updated_time(self, obj):
        return datetime.strftime(obj.updated_time, CUSTOM_DATETIME_FORMAT_WITH_TIMEZON)


admin.site.register(ShortenedUrl, ShortenedUrlAdmin)
