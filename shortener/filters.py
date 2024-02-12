from django_filters import rest_framework as filters
from .models import ShortenedUrlStatistics


class ShortenedUrlStatisticsFilter(filters.FilterSet):
    min_clicked = filters.NumberFilter(field_name="clicked", lookup_expr="gte")
    max_clicked = filters.NumberFilter(field_name="clicked", lookup_expr="lte")
    start_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="date", lookup_expr="lt")

    class Meta:
        model = ShortenedUrlStatistics
        fields = ["shortened_url"]
