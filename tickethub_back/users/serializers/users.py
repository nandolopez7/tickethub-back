"""Users serializers."""
from datetime import datetime

# Django
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.signals import user_logged_in
from django.core import exceptions

# Django REST Framework
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Models
from tickethub_back.users.models import User
from django.contrib.auth.models import Group

# Logic
from tickethub_back.users.logic.user import UserLogic

# Utils
from django.utils import timezone
from tickethub_back.users.models.users import BloquedUser
from tickethub_back.utils.custom_regex_validators import CellNumberRegexValidator
from tickethub_back.utils.serializers.globals import DataChoiceSerializer


class UserModelSerializer(serializers.ModelSerializer):

    identification_type = DataChoiceSerializer()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'is_active', 'created', 'updated',
            'email', 'identification_number', 'identification_type', 'birth_date',
            'phone_number', 'groups', 'photo', 'username', 'photo_google'
        ]


"""
Login serializers
"""

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    """User login serializer"""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError({'detail': 'Credenciales invalidas.'})
        
        user_bloqued = BloquedUser.objects.filter(user=user, fecha_vigencia_bloqueo__gte=datetime.now()).first()
        if user_bloqued:
            raise serializers.ValidationError({'detail': 'Cuenta bloqueada. {}'.format(user_bloqued.observacion)})

        if not user.is_active:
            raise serializers.ValidationError({'detail': 'Cuenta no activa, por favor comuniquese con el administrador.'})
        self.context['user'] = user
        return super().validate(data)

    def create(self, data):
        """Generate or retrieve new token."""
        token = super().get_token(self.context['user'])
        token['obj_user'] = UserModelSerializer(self.context['user']).data

        user = self.context['user']
        request = self.context['request']
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        token = {
            'refresh': str(token),
            'access': str(token.access_token)
        }
        return self.context['user'], token


class UserTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        help_text="Token de mayor duración que puede ser usado para obtener un nuevo token de acceso."
    )
    access = serializers.CharField(
        help_text="Token de acceso que debe ser enviado en la cabecera de todas las demás API's."
    )


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is invalid or expired'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class UserLoginSerializer(serializers.Serializer):
    user = UserModelSerializer()
    token = UserTokenSerializer()


class ValidateSendResetPassword(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError(
                "No pudimos encontrar una cuenta asociada con ese correo electrónico. Pruebe con una dirección de correo electrónico diferente."
            )
        
        user_bloqued = BloquedUser.objects.filter(user=user, fecha_vigencia_bloqueo__gte=datetime.now()).first()
        if user_bloqued:
            raise serializers.ValidationError({'detail': 'Cuenta bloqueada. {}'.format(user_bloqued.observacion)})
        return email


class ConfirmResetPassword(ValidateSendResetPassword):
    password = serializers.CharField()
    codigo = serializers.IntegerField()


class UpdateAndCreateUserSerializer(serializers.ModelSerializer):
    """
    Update and create user serializer.
    """
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), 
        lookup='icontains')]
    )
    cel_number_regex = CellNumberRegexValidator(
        message="El formato permitido es 3112224455"
    )
    phone_number = serializers.CharField(validators=[cel_number_regex], max_length=10, required=False)
    identification_number =  serializers.IntegerField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        min_value=111111,
        max_value=9999999999,
        required=False
    )
    identification_type = serializers.ChoiceField(
        choices=User.IdentificationTypeChoices.choices,
        default=User.IdentificationTypeChoices.CC
    )
    birth_date = serializers.DateField(required=False)
    password = serializers.CharField(min_length=6, max_length=30)
    
    # Relación m2m con la tabla de grupos, conocida tambien como "rol"
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        default=2
    )

    class Meta:
        """Meta class."""
        model = User
        fields = '__all__'       

    def validate(self, data):
        password = data.get('password', False)
        if password:
            errors = dict()
            try:
                """ Cuando es actualizacion de contraseña, solo se recibe el password, por eso se usa self.instance """
                if self.instance:
                    user = self.instance
                else:
                    """Cuando es un usuario nuevo, se usa los datos entrantes"""
                    user_data = data.copy()
                    user_data.pop('user_permissions', None)
                    user_data.pop('groups', None)
                    user = User(**user_data)

                password_validation.validate_password(password=password, user=user)
            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)

                if errors:
                    raise serializers.ValidationError(errors)
                
        return super().validate(data)

    def create(self, data):
        """
        Crear usuario
        """
        data['is_active'] = True
        return UserLogic.create_user(data)

    def update(self, instance, data):
        user = super().update(instance=instance, validated_data=data)
        try:
            user.set_password(data['password'])
            user.password_change_date = timezone.now()
            user.save()
        except KeyError:
            pass
        return user