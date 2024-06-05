"""Events urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from tickethub_back.events import views
from tickethub_back.events.views.buy_event_tickets import BuyEventTicketViewSet

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event'),
router.register(r'buy-ticket-event', BuyEventTicketViewSet, basename='buy-ticket-event')

urlpatterns = [
    path('', include(router.urls)),
]