from rest_framework.exceptions import APIException


class PermissionFormatError(APIException):
    default_detail = ('permission should be in list format')

class UnKnownPermissionType(APIException):
    # def __init__(self,error):
    #     self._error = error
    default_detail = ('unknown permission type')