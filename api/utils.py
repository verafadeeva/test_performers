from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.views import exception_handler
from rest_framework.serializers import as_serializer_error
from rest_framework import exceptions


def custom_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        error = exc.error_dict.pop('__all__')
        exc.error_dict['detail'] = error
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, context)

    if response is None:
        return response

    return response
