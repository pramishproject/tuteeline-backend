from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    handler = {
        'ParseError': _handle_generic_error,
        'AuthenticationFailed': _handle_generic_error,
        'NotAuthenticated': _handle_generic_error,
        'PermissionDenied': _handle_generic_error,
        'NotFound': _handle_generic_error,
        'MethodNotAllowed': _handle_generic_error,
        'NotAcceptable': _handle_generic_error,
        'UnsupportedMediaType': _handle_generic_error,
        'ValidationError': _handle_generic_error,
        'ZeroDivisionError': _handle_generic_error
    }
    response = exception_handler(exc, context)
    print("erroororhandler**********************", response)
    exception_class = exc.__class__.__name__
    print(exception_class)
    if response is not None:
        response.data['status_code'] = response.status_code

    if exception_class in handler:
        return handler[exception_class](exc, context, response)
    return Response({"error": str(exc), "status": False}, status="400")


def _handle_generic_error(exc, context, response):
    print("*****<<<", context)
    return Response({"message": str(exc)})
