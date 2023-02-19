import django_filters
from card.models import Card

class CardFilter(django_filters.FilterSet):

    class Meta:
        model = Card
        fields = {
            'series_card': ['exact'],
            'number_card': ['exact'],
            'date_start_card': ['exact'],
            'date_end_active_card': ['exact'],
            'status_card': ['exact'],
        }
