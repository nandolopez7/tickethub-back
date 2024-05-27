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

    name = models.TextField(max_length=150, verbose_name='Name')
    date = models.DateField(
        'Event Date', help_text='Date the event will take place.'
    )
    time = models.TimeField(
        'Event Time', help_text='Time the event will take place.'
    )
    place = models.TextField(max_length=250, verbose_name='Place')
    file_cover = models.URLField(null=True)
    is_active = models.BooleanField(default=True)

    objects = EventManager()

    def __str__(self):
        return "Event id: {} name: {} ".format(
            self.id, self.name)
    
    class Meta:
        db_table = 'event'
        managed = True
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
