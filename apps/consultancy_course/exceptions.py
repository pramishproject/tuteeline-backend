from rest_framework.exceptions import NotFound
from django.utils.translation import gettext_lazy as _

class ConsultancyCourseNotFound(NotFound):
    default_detail = _("course doesnt exist for following id")