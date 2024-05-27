"""Views event."""
# Django
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Sum


# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

# Swagger
from drf_yasg.utils import swagger_auto_schema

# Models
from tickethub_back.events.models import Event

# Serializers
from tickethub_back.events import serializers

#Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from tickethub_back.events.filter import EventFilter
from tickethub_back.events.serializers.events import EventModelSerializer, ValidateUserEntrySerializer
from tickethub_back.users.models.users import User
from tickethub_back.utils.custom_exceptions import CustomAPIException


@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    auto_schema=None
))
class EventViewSet(mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    """
    API de eventos
    """

    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description']
    filterset_class = EventFilter

    def get_serializer_class(self):
        return serializers.EventModelSerializer

    def get_permissions(self):
        # if self.action in ['login', 'password_reset', 'confirm_password_reset']:
        #     """ Cuando en 'Login' no se solicita al evento estar autenticado """
        #     permissions = [AllowAny]
        # else:
        #     permissions = [IsAuthenticated]
        permissions = [AllowAny]
        return [permission() for permission in permissions]

    def list(self, request, *args, **kwargs):
        """ Listar eventos

            Permite listar todos los eventos registrados en el sistema.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consultar evento por ID

            Permite obtener información de un evento dado su ID
        """
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Crear eventos

            Permite crear eventos a ls podran asistir los usuarios
        """
        print("*** datos recibidos del eventos: ", request.data)
        serializer = serializers.UpdateAndCreateEventSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        data = self.get_serializer(instance=event).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """ Actualizar eventos
        
            Perimite la actualización de un evento dado su ID.
        """
        print("*** datos recibidos del eventos: ", request.data)
        event = self.get_object()
        serializer = serializers.UpdateAndCreateEventSerializer(
            instance=event,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        data = self.get_serializer(instance=event).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        """Disable event."""
        instance.is_active = False
        instance.save()
