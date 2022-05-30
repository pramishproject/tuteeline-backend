from django.views import generic

from apps.notification.mixins import NotificationMixin


class PortalReceiveNotificationView(generic.TemplateView):
    template_name = 'portal_receive.html'


class ConsultancyReceiveNotificationView(generic.TemplateView):
    template_name = 'consultancy_receive.html'


class SendNotificationView(generic.TemplateView, NotificationMixin):
    notification_group = ['portal_user', 'consultancy_user']
    template_name = 'send.html'

    def get(self, request, *args, **kwargs):
        self.send_notification()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_notification_data(self):
        return {
            'message': 'Hello World'
        }
