
# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from .base import DateBaseModel

class City(DateBaseModel):

    name = models.CharField(max_length=30, null=False)
    department = models.ForeignKey('utils.Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta(DateBaseModel.Meta):
        db_table = 'cities'
        managed = True
        verbose_name = 'city'
        verbose_name_plural = 'cities'