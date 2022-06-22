from apps.academic import usecases
class AcademicMixins:
    def get_academic(self):
        return usecases.GetStudentAcademicUseCase(
            academic_id = self.kwargs.get("academic_id")
        ).execute()

class GetSopMixin:
    def get_sop(self):
        return usecases.GetSopByIdUseCase(
            id = self.kwargs.get("sop_id")
        ).execute()
class SopMixins:
    def get_sop(self):
        return usecases.GetSopUseCase(
            student=self.kwargs.get("student_id")
        ).execute()

class LorMixins:
    def get_lor(self):
        return usecases.GetLorUseCase(
            lor=self.kwargs.get("lor_id")
        ).execute()

class EssayMixins:
    def get_essay(self):
        return usecases.GetEssayUseCase(
            student_id = self.kwargs.get("student_id")
        ).execute()

class GetEssayMixins:
    def get_essay(self):
        return usecases.GetEssayByIdUseCase(
            essay_id = self.kwargs.get("essay_id")
        ).execute()