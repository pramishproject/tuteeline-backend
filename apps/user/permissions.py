from rest_framework.permissions import BasePermission

from apps.institute.models import InstituteStaff
from apps.staff.exceptions import PermissionFormatError
from apps.user.models import InstituteUser
from django.contrib.auth import get_user_model
User  = get_user_model()
class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and not user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)

class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.user_type == "student_user":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)


class IsInstituteUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.user_type == "institute_user":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)


class CheckPermission:
    def __init__(self,permissions:list,user:User):
        self._permission = permissions
        self._user  = user
    def has_permission(self):
        staff = InstituteStaff.objects.get(user=self._user)
        self.lst1 = self._permission
        self.lst2 = staff.role.permission_list
        if not isinstance(self.lst1, dict):
            return False
        if not isinstance(self.lst2, dict):
            return False

        present = self.intersection()
        if len(present)>0:
            return True
        else:
            return False
    def intersection(self):
        return list(set(self.lst1) & set(self.lst2))


# class InitInstitute(BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         if user.user_type == "institute_user":
#             return True
#         return False
#
#     def has_object_permission(self, request, view):
#         return request.user
# class IsSuperUser(BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         if user.user_type == "institute_user":
#             staff  = InstituteStaff.objects.get(user=user)
#             if staff.role.name == ""
#             return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         return bool(request.user == obj)
class IsConsultancyUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.user_type == "consultancy_user":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print("*************obj",obj)
        return bool(request.user == obj)


