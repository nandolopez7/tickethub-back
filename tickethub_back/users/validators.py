from django.core.exceptions import (ValidationError, FieldDoesNotExist,)
try:
    from django.utils.translation import gettext as _, ngettext
except ImportError:
    from django.utils.translation import ugettext as _, ungettext as ngettext

import re
from difflib import SequenceMatcher


class CustomPasswordCharacterValidator():

    def __init__(
            self,
            min_length_digit=1,
            min_length_alpha=1,
            min_length_special=1,
            min_length_lower=1,
            min_length_upper=1,
            special_characters="~!@#$%^&*()_+{}\":;'[]"
    ):
        self.min_length_digit = min_length_digit
        self.min_length_alpha = min_length_alpha
        self.min_length_special = min_length_special
        self.min_length_lower = min_length_lower
        self.min_length_upper = min_length_upper
        self.special_characters = special_characters

    def validate(self, password, user=None):
        validation_errors = []
        if len([char for char in password if char.isdigit()]) < self.min_length_digit:
            validation_errors.append(ValidationError(
                ngettext(
                    'Su contraseña debe contener por lo menos %(min_length)d número.',
                    'Su contraseña debe contener por lo menos %(min_length)d números.',
                    self.min_length_digit
                ),
                params={'min_length': self.min_length_digit},
                code='min_length_digit',
            ))
        if len([char for char in password if char.isalpha()]) < self.min_length_alpha:
            validation_errors.append(ValidationError(
                ngettext(
                    'Su contraseña debe contener por lo menos %(min_length)d letra.',
                    'Su contraseña debe contener por lo menos %(min_length)d letras.',
                    self.min_length_alpha
                ),
                params={'min_length': self.min_length_alpha},
                code='min_length_alpha',
            ))
        if len([char for char in password if char.isupper()]) < self.min_length_upper:
            validation_errors.append(ValidationError(
                ngettext(
                    'Su contraseña debe contener por lo menos %(min_length)d letra mayúscula.',
                    'Su contraseña debe contener por lo menos %(min_length)d letras mayúsculas.',
                    self.min_length_upper
                ),
                params={'min_length': self.min_length_upper},
                code='min_length_upper_characters',
            ))
        if len([char for char in password if char.islower()]) < self.min_length_lower:
            validation_errors.append(ValidationError(
                ngettext(
                    'Su contraseña debe contener por lo menos %(min_length)d letra minúscula.',
                    'Su contraseña debe contener por lo menos %(min_length)d letras minúsculas.',
                    self.min_length_lower
                ),
                params={'min_length': self.min_length_lower},
                code='min_length_lower_characters',
            ))
        if len([char for char in password if char in self.special_characters]) < self.min_length_special:
            validation_errors.append(ValidationError(
                ngettext(
                    'Su contraseña debe contener por lo menos %(min_length)d carácter especial.',
                    'Su contraseña debe contener por lo menos %(min_length)d caracteres especiales.',
                    self.min_length_special
                ),
                params={'min_length': self.min_length_special},
                code='min_length_special_characters',
            ))
        if validation_errors:
            raise ValidationError(validation_errors)

    def get_help_text(self):
        validation_req = []
        if self.min_length_alpha:
            validation_req.append(
                ngettext(
                    "%(min_length)s letra",
                    "%(min_length)s letras",
                    self.min_length_alpha
                ) % {'min_length': self.min_length_alpha}
            )
        if self.min_length_digit:
            validation_req.append(
                ngettext(
                    "%(min_length)s número",
                    "%(min_length)s números",
                    self.min_length_digit
                ) % {'min_length': self.min_length_digit}
            )
        if self.min_length_lower:
            validation_req.append(
                ngettext(
                    "%(min_length)s letra minúscula",
                    "%(min_length)s letras minúsculas",
                    self.min_length_lower
                ) % {'min_length': self.min_length_lower}
            )
        if self.min_length_upper:
            validation_req.append(
                ngettext(
                    "%(min_length)s letra mayúscula",
                    "%(min_length)s letras mayúsculas",
                    self.min_length_upper
                ) % {'min_length': self.min_length_upper}
            )
        if self.special_characters:
            validation_req.append(
                ngettext(
                    "%(min_length_special)s carácter especial como: %(special_characters)s",
                    "%(min_length_special)s carácteres especiales como: %(special_characters)s",
                    self.min_length_special
                ) % {'min_length_special': str(self.min_length_special), 'special_characters': self.special_characters}
            )

        if len(validation_req) > 1:
            last_validation = validation_req.pop()
            return _("Su contraseña debe contener por lo menos") + ' {} y {}.'.format(
                ', '.join(validation_req),  last_validation)

        return _("Su contraseña debe contener por lo menos") + ' ' + ', '.join(validation_req) + '.'


class UserAttributeSimilarityValidator:
    """
    Clase que permite validar si hay coincidecias en la contraseña y algunos atributos del usuario
    """
    DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("Por favor, ingrese una nueva contraseña y recuerde seguir las recomendaciones"
                          " para crear una contraseña segura."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return _("Your password can't be too similar to your other personal information.")
