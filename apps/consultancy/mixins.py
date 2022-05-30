from apps.consultancy.usecases import GetConsultancyUseCase, GetConsultancyStaffUseCase


class ConsultancyMixin:
    def get_consultancy(self):
        return GetConsultancyUseCase(consultancy_id=self.kwargs.get('consultancy_id')).execute()


class ConsultancyStaffMixin:
    def get_consultancy_staff(self):
        return GetConsultancyStaffUseCase(consultancy_staff_id=self.kwargs.get('consultancy_staff_id')).execute()
