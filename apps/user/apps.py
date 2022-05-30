from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    name = "apps.user"
    verbose_name = _("Users")

    def ready(self):
        try:
            import apps.user.recievers  # noqa F401
        except ImportError:
            pass
