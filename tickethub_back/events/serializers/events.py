"""Events serializers."""

from datetime import datetime, time

# Django REST Framework
from rest_framework import serializers

# Models
from tickethub_back.events.models import Event


# Serializers
from tickethub_back.users.models.users import User
from tickethub_back.utils.serializers.globals import DataSerializer
from tickethub_back.users.serializers.users import UserModelSerializer


class EventModelSerializer(serializers.ModelSerializer):
    city = DataSerializer()
    organizer = UserModelSerializer()
    event_type = DataSerializer()
    info_event = serializers.SerializerMethodField()

    def get_info_event(self, obj):
        time_value = time(obj.time.hour, obj.time.minute, obj.time.second)
        time_difference = datetime.combine(obj.date, time_value) - datetime.now()

        days = time_difference.days
        days = 0 if days < 0 else days
        hours = time_difference.seconds // 3600

        if hours > 1:
            return f"El evento está a {days} días y {hours} horas de iniciar"
        
        if hours == 1:
            return f"El evento está a {days} días y {hours} hora de iniciar"
        
        if hours < 0 and hours > -5:
            return "El evento inició"

        return "El evento a pasado"


    class Meta:
        model = Event
        fields = '__all__'


class UpdateAndCreateEventSerializer(serializers.ModelSerializer):
    """
    Update and create event serializer.
    """
    file_cover = serializers.FileField(required=True)

    class Meta:
        """Meta class."""
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        validated_data["is_active"] = True
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ValidateUserEntrySerializer(serializers.Serializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    user_photo = serializers.FileField()