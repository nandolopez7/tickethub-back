
# Django
from django.db import models

# Utilities
from .base import DateBaseModel

class Department(DateBaseModel):
    name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.name

    class Meta(DateBaseModel.Meta):
        db_table = 'departments'
        managed = True
        verbose_name = 'department'
        verbose_name_plural = 'departments'