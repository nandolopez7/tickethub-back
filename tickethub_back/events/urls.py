"""Events urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from tickethub_back.events import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]