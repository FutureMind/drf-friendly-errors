from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

from rest_framework_friendly_errors import settings
from rest_framework_friendly_errors.utils import is_pretty


def friendly_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if not response and settings.CATCH_ALL_EXCEPTIONS:
        response = exception_handler(APIException(exc), context)

    if response is not None:
        if is_pretty(response):
            return response
        error_message = response.data['detail']
        error_code = settings.FRIENDLY_EXCEPTION_DICT.get(
            exc.__class__.__name__)
        response.data.pop('detail', {})
        response.data['code'] = error_code
        response.data['message'] = error_message
        response.data['status_code'] = response.status_code
        # response.data['exception'] = exc.__class__.__name__

    return response
