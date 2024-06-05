
# Django
from django_filters.rest_framework import BaseInFilter, NumberFilter, DateFilter
import rest_framework_filters as filters

from tickethub_back.events.models.buy_event_tickets import BuyEventTicket


# Models
from .models.events import Event


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class EventFilter(filters.FilterSet):
    created__gte = DateFilter(field_name='created', lookup_expr='date__gte')
    created__lte = DateFilter(field_name='created', lookup_expr='date__lte')

    class Meta:
        model = Event
        fields = [
            'created__gte', 'created__lte', 'is_active'
        ]



class BuyEventTicketFilter(filters.FilterSet):
    assistant = NumberInFilter(field_name='assistant', lookup_expr='in')
    event = NumberInFilter(field_name='event', lookup_expr='in')
    category = NumberInFilter(field_name='category', lookup_expr='in')

    class Meta:
        model = BuyEventTicket
        fields = [
            'assistant', 'event', 'category'
        ]
