"""Events serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from tickethub_back.events.models.buy_event_tickets import BuyEventTicket

# Serializers
from tickethub_back.utils.serializers.globals import DataChoiceSerializer
from tickethub_back.users.serializers.users import UserModelSerializer
from tickethub_back.events.serializers.events import EventModelSerializer


class BuyEventTicketModelSerializer(serializers.ModelSerializer):
    category = DataChoiceSerializer()
    event = EventModelSerializer()

    class Meta:
        model = BuyEventTicket
        fields = '__all__'


class UpdateAndCreateBuyEventTicketSerializer(serializers.ModelSerializer):
    """
    Update and create event serializer.
    """

    total_cost = serializers.FloatField(required=False)

    def validate(self, data):
        data['total_cost'] = data['cost'] * data['number']
        return data

    class Meta:
        """Meta class."""
        model = BuyEventTicket
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
