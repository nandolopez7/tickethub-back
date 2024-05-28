"""Events urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from tickethub_back.utils import views

router = DefaultRouter()
router.register(r'utils/rekognition', views.RekognitionViewSet, basename='utils')

urlpatterns = [
    path('', include(router.urls)),
]