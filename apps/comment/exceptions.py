from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound


class CommentNotFound(NotFound):
    default_detail = _('Comment Not Found')