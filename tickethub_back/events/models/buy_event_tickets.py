"""Costo de tiquetes del evento model."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Models
from tickethub_back.utils.models.base import DateBaseModel


class BuyEventTicket(DateBaseModel):

    class CategoryChoices(models.TextChoices):
        GENERAL = 1, _('GENERAL')
        VIP = 2, _('VIP')

    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    category = models.CharField(
        choices=CategoryChoices.choices,
        max_length=1,
        default=CategoryChoices.GENERAL
    )
    number = models.IntegerField()
    cost = models.FloatField()
    total_cost = models.FloatField()
    assistant = models.ForeignKey('users.User', on_delete=models.RESTRICT)

    def __str__(self):
        return "BuyEventTicket id: {} event: {} ".format(
            self.id, self.event)
    
    class Meta:
        db_table = 'buy_event_tickets'
        managed = True
        verbose_name = 'Buy Event Ticket'
        verbose_name_plural = 'Buy Event Tickets'
