# Rest Framework
from rest_framework import status
from rest_framework import exceptions


class CustomAPIException(exceptions.APIException):
    """CustomAPIException.

    Esta excepción retorna un Response.
    """

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail, status_code=None):
        self.default_detail = detail
        if status_code:
            self.status_code = status_code
        super(CustomAPIException, self).__init__()