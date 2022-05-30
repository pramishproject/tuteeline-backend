from apps.user.usecases import consultancy_user_usecases, portal_user_usecases,institute_user_usecases


class ConsultancyUserMixin:
    def get_consultancy_user(self):
        return consultancy_user_usecases.GetConsultancyUserUseCase(
            consultancy_user_id=self.kwargs.get('consultancy_user_id')
        ).execute()


class PortalUserMixin:
    def get_portal_user(self):
        return portal_user_usecases.GetPortalUserUseCase(
            portal_user_id=self.kwargs.get('portal_user_id')
        ).execute()

class InstituteUserMixin:
    def get_institute_user(self):
        return institute_user_usecases.GetInstituteUserUseCase(
            institute_user_id=self.kwargs.get('institute_user_id')
        ).execute()
