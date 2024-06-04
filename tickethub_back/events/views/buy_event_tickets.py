"""Views event."""
# Django
from django.utils.decorators import method_decorator
from django.db import transaction

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

# Swagger
from drf_yasg.utils import swagger_auto_schema

# Models
from tickethub_back.events.models.buy_event_tickets import BuyEventTicket

# Serializers
from tickethub_back.events.serializers.buy_events_tickets import serializers
from tickethub_back.events.serializers.buy_events_tickets import UpdateAndCreateBuyEventTicketSerializer, BuyEventTicketModelSerializer

#Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from tickethub_back.events.filter import BuyEventTicketFilter


@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    auto_schema=None
))
class BuyEventTicketViewSet(mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    """
    API de eventos
    """

    queryset = BuyEventTicket.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['event__name', 'eventt__description']
    filterset_class = BuyEventTicketFilter

    def get_serializer_class(self):
        return BuyEventTicketModelSerializer

    def get_permissions(self):
        # if self.action in ['login', 'password_reset', 'confirm_password_reset']:
        #     """ Cuando en 'Login' no se solicita al evento estar autenticado """
        #     permissions = [AllowAny]
        # else:
        #     permissions = [IsAuthenticated]
        permissions = [AllowAny]
        return [permission() for permission in permissions]

    def list(self, request, *args, **kwargs):
        """ Listar compra de tickets

            Permite listar todas las compras de tickets a eventos registrados en el sistema.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consultar compra de ticket por ID

            Permite obtener información de una compra de ticket de evento dado su ID
        """
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Crear compra de ticket a eventos

            Permite crear compra de ticket a eventos
        """
        print("*** datos recibidos del compra ticket: ", request.data)
        serializer = UpdateAndCreateBuyEventTicketSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        data = self.get_serializer(instance=event).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """ Actualizar compra de ticket a eventos
        
            Perimite la actualización de una compra de ticket de evento dado su ID.
        """
        event = self.get_object()
        serializer = UpdateAndCreateBuyEventTicketSerializer(
            instance=event,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        data = self.get_serializer(instance=event).data
        return Response(data=data, status=status.HTTP_201_CREATED)
