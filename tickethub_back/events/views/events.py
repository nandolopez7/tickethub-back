"""Views event."""
from datetime import datetime
# Django
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Sum

try:
    from django.utils.translation import gettext as _
except ImportError:
    from django.utils.translation import ugettext as _

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
from tickethub_back.events.models.buy_event_tickets import BuyEventTicket
from tickethub_back.utils.custom_exceptions import CustomAPIException
from tickethub_back.utils.logic.rekognition import RekognitionLogicClass


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

    queryset = Event.objects.filter(date__gte=datetime.now().date()).all()
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

    @action(detail=False, methods=['POST'])
    def validate_user_entry(self, request, *args, **kwargs):
        
        serializer = ValidateUserEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data
        image_source = data['user_photo']

        rekognition = RekognitionLogicClass(image_source=image_source)

        """ Validar que en la foto haya un rostro """
        try:
            rekognition.detect_faces()
        except CustomAPIException as err:
            return Response(err.default_detail, status=err.status_code)

        """ Buscar todas las compras asociadas a este evento """
        purchased_tickets = BuyEventTicket.objects.filter(event=data['event']).order_by('-id')

        """ Obtener el usaurio de cada compra y comparar su foto con la recibida en la validación """
        for buy_ticket in purchased_tickets:
            if buy_ticket.assistant.photo is None or buy_ticket.assistant.photo == "":
                continue

            image_target = buy_ticket.assistant.photo
            event = buy_ticket.event
            try:
                
                data_response = rekognition.compare_faces(image_target)

                """ Si se hace match, se valida que el evento corresponda al mismo que se recibió """
                if data_response['ok'] is True:
                    is_same_event = (event.id == int(data['event']))
                    data_result = {
                        'ok': is_same_event,
                        'data': {
                            'event': EventModelSerializer(instance=event).data,
                            'similarity': data_response['data']['similarity'],
                        },
                        'message': _("Validación exitosa") if is_same_event else _("No corresponde al mismo evento")
                    }
                    return Response(data_result, status=status.HTTP_200_OK)
            except CustomAPIException as err:
                pass

        data = {
            'ok': False,
            'data': None,
            'message': _("No se encontró coincidencias")
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def assistant_user_events(self, request,  *args, **kwargs):
        """ Validar usuario """
        if isinstance(request.user, User):  # cuando el usuario es de sesión (enviado en el HEADER de la petición)
            user_obj = request.user  
        else:
            user_id = request.GET.get('user')  # cuando el usuario es enviado por parametro en la URL
            user_obj = User.objects.filter(id=user_id).first()
        
        if user_obj is None:
            return Response(data={'detail': [_("Usuario no encontrado")]}, status=status.HTTP_400_BAD_REQUEST)
        
        """ Consultar los distintos eventos a los cuales un usuario a comprado tickets """
        events = Event.objects.filter(
            buyeventticket__assistant=user_obj
        ).distinct()

        """ Serializar listado de eventos (JSON) """
        data = self.get_serializer(instance=events, many=True).data

        """ Agregar información sobre total de tickets y total de compra por cada evento """
        for event_item in data:
            event_item['tickets'] = BuyEventTicket.objects.filter(assistant=user_obj, event_id=event_item['id']) \
            .annotate(
                number_of_tickest=Sum('number'),
                total=Sum('total_cost')
            ).values('number_of_tickest', 'total').first()

        return Response(data=data, status=status.HTTP_200_OK)