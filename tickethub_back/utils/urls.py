"""Events urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from tickethub_back.utils import views

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
]