from apps.review.usecases import GetInstituteReviewByIdUseCase


class InstituteReviewMixins:
    def get_Institute_review(self):
        return GetInstituteReviewByIdUseCase(
            institute_review_id=self.kwargs.get('institute_review_id')
        ).execute()