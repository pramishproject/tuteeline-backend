from apps.counselling.usecases import GetCounselling, GetConsultancyCounselling


class InstituteCounsellingMixin:
    def get_counselling(self):
        return GetCounselling(counselling_id=self.kwargs.get('counselling_id')).execute()

class ConsultancyCounsellingMixin:
    def get_consultancy_counselling(self):
        return GetConsultancyCounselling(consultancy_counselling_id=self.kwargs.get('consultancy_counselling_id')).execute()