from apps.institute import usecase

class InstituteMixins:
    def get_institute(self):
        return usecase.GetInstituteUseCase(
            institute_id=self.kwargs.get('institute_id')
        ).execute()

class ScholorshipMixins:
    def get_scholorship(self):
        return usecase.GetScholorshipUseCase(
            scholorship_id = self.kwargs.get('scholorship_id')
        ).execute()

class SocialMediaMixins:
    def get_socialmedia(self):
        return usecase.GetSocialMedia(
            socialmedia_id = self.kwargs.get('socialmedia_id')
        ).execute()

class FacilityMixin:
    def get_facility(self):
        return usecase.FacilityUseCase(
            facility_id = self.kwargs.get("facility_id")
        ).execute()