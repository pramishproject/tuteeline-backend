from apps.counselling.usecases import GetCounselling


class InstituteCounsellingMixin:
    def get_counselling(self):
        return GetCounselling(counselling_id=self.kwargs.get('counselling_id')).execute()

