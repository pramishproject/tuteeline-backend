# from apps.consultancy.usecases import GetConsultancyUseCase
# from apps.portal.usecases import GetPortalUseCase


# class PortalMixin:
#     def get_portal(self):
#         return GetPortalUseCase(portal_id=self.kwargs.get('portal_id')).execute()

from apps.portal.usecases import GetPortalUserByIdUseCase


class PortalStaffUserMixin:
    def get_portal_staff(self):
        return GetPortalUserByIdUseCase(
            user_id=self.kwargs.get('staff_id')
        )
