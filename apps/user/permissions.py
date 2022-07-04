from rest_framework.permissions import BasePermission


class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print("************user",user.pk,view)
        return bool(user.is_authenticated and not user.is_staff)

    def has_object_permission(self, request, view, obj):
        print("*************obj",obj)
        return bool(request.user == obj)

class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.user_type == "student_user":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print("*************obj",obj)
        return bool(request.user == obj)

class IsInstituteUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.user_type == "institute_user":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print("*************obj",obj)
        return bool(request.user == obj)

class IsConsultancyUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.user_type == "consultancy_user":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print("*************obj",obj)
        return bool(request.user == obj)


