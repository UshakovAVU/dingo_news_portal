import django_filters
from .models import News
from django.forms import DateInput

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    publish_date = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), lookup_expr='gte')

    class Meta:
        model = News
        fields = ['title', 'author', 'publish_date']
