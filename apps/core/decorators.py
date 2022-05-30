from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from rest_framework import exceptions
from django.core.exceptions import PermissionDenied


def student_required(function=None):
    def wrapper(request, *args, **kwargs):
        print("in wrapper", request.user.is_student)
        is_student = request.user.is_student
        if not is_student:
            raise exceptions.AuthenticationFailed('This is not authorized user')
        else:
            return function(request)

    return wrapper


def college_required(function=None):
    def wrapper(request, *args, **kwargs):
        print("in wrapper", request.user.is_institute)
        is_institute = request.user.is_institute
        if not is_institute:
            raise exceptions.AuthenticationFailed('This is not authorized user')
        else:
            return function(request)

    return wrapper
