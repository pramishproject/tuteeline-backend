from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, APIException

class InstituteNotFound(NotFound):
    default_detail = _('institute not found')

class CourseNotFound(NotFound):
    default_detail = _('course not found')

class FacultyNotFound(NotFound):
    default_detail = _('faculty not found')

class VoucherNotFound(NotFound):
    default_code = _("voucher not found")

class InstituteApplyNotFound(NotFound):
    default_detail = _("student application not found following id")

             
class InstituteStaffNotFound(NotFound):
    default_detail = _("staff not found following id")

class UniqueStudentApply(NotFound):
    default_detail = _("Student Already apply this course")

class CheckDocumentDoesntExist(NotFound):
    default_detail = _("document doesnt exist")



class DocTypeNotFound(APIException):
    status_code = 204
    default_detail = 'document type not found'
    default_code = 'service_unavailable'