from apps.review.usecases import GetInstituteReviewByIdUseCase, GetConsultancyReviewByIdUseCase


class InstituteReviewMixins:
    def get_Institute_review(self):
        return GetInstituteReviewByIdUseCase(
            institute_review_id=self.kwargs.get('institute_review_id')
        ).execute()

class ConsultancyReviewMixins:
    def get_consultancy_review(self):
        return GetConsultancyReviewByIdUseCase(
            consultancy_review_id = self.kwargs.get('consultancy_review_id')
        ).execute()