"""Invitados model."""

# Django
from django.db import models

# Models
from tickethub_back.utils.models.base import DateBaseModel


def directory_path(instance, filename):
    return 'files/events/{0}/{1}'.format(instance.date, filename)


class EventManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)
    

class Event(DateBaseModel):

    class CategoryChoices(models.TextChoices):
        COMEDIA = 'Comedia'
        FESTIVAL = 'Festival'
        EXPOSICION = 'Exposición'
        DEPORTES = 'Deportes'
        CONCIERTO = 'Concierto'

    name = models.TextField(max_length=150, verbose_name='Name')
    date = models.DateField(
        'Event Date', help_text='Date the event will take place.', null=True
    )
    time = models.TimeField(
        'Event Time', help_text='Time the event will take place.', null=True
    )
    place = models.TextField(max_length=250, verbose_name='Place')
    file_cover = models.URLField(null=True)
    is_active = models.BooleanField(default=True)

    description = models.TextField(max_length=150, verbose_name='Description', blank=True)
    category = models.CharField(max_length=30, choices=CategoryChoices.choices)
    price = models.BigIntegerField(default=10)

    objects = EventManager()

    def __str__(self):
        return "Event id: {} name: {} ".format(
            self.id, self.name)
    
    class Meta:
        db_table = 'event'
        managed = True
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
