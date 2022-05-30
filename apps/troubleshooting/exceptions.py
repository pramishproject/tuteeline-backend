from rest_framework.exceptions import NotFound


class TroubleshootNotFound(NotFound):
    default_detail = 'Troubleshoot id not found for following id.'
