"""User model."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager

from tickethub_back.utils.models.base import DateBaseModel

# Utilities


class MyUserManager(BaseUserManager):
    """
        Manager encargado de la creacion de super usuarios.
    """

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email, is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(DateBaseModel, AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    class IdentificationTypeChoices(models.TextChoices):
        CC = 1, _('CÉDULA DE CIUDADANíA')
        CE = 2, _('CÉDULA DE EXTRANGERIA')
        NIT = 3, _('NÚMERO DE IDENTIFICACIÓN TRIBUTARIA')

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists'
        }
    )

    phone_number = models.CharField(max_length=10, blank=True)
    identification_number = models.BigIntegerField(null=True)
    identification_type = models.CharField(
        choices=IdentificationTypeChoices.choices,
        default=IdentificationTypeChoices.CC,
        max_length=1, null=True, blank=True
    )
    birth_date = models.DateField(null=True)
    photo = models.ImageField(
        null=True,
        upload_to='files/users/pictures/',
    )

    username = models.CharField(
        max_length=150,
        null=True,
        unique=True,
    )

    photo_google = models.CharField(max_length=250, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name', 
        'last_name', 
        'identification_number', 
        'identification_type'
    ]

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email
    

class BloquedUser(DateBaseModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
    )
    fecha_vigencia_bloqueo = models.DateTimeField(blank=True, null=True)
    observacion = models.TextField(max_length=250, verbose_name='Observación', blank=True)

    def __str__(self):
        return "BloquedUser id: {} fecha_vigencia_bloqueo: {} observacion: {} ".format(
            self.id, self.fecha_vigencia_bloqueo, self.observacion)
    

    class Meta(DateBaseModel.Meta):
        db_table = 'bloqued_users'
        managed = True
        verbose_name = 'bloqued_users'
        verbose_name_plural = 'bloqued_users'
