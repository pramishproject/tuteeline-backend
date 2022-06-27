from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, APIException

class InstituteUserEmailNotFound(NotFound):
    default_detail = _('Institute user   not  found for following email.')

class InstituteNotFound(NotFound):
    default_detail = _('Institute   not  found for following id.')

class StaffNotFound(NotFound):
    default_detail = _('Institute  staff not  found for following id.')

class InstituteScholorshipDoesntExist(NotFound):
    default_detail = _("scholorship doesnt exist")

class SocialMediaLinkDoesntExist(NotFound):
    default_detail = _("social media doesnt exist")

class FacilityDoesntExist(NotFound):
    default_detail = _("facility doesnt exist")