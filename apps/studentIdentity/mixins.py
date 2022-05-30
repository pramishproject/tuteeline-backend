from apps.studentIdentity import usecases

class CitizenshipMixins:
    def get_citizenship(self):
        return usecases.GetCitizenshipUseCase(
            student_id=self.kwargs.get('student_id')
        ).execute()

class PassportMixins:
    def get_passport(self):
        return usecases.GetPassportUseCase(
            student_id=self.kwargs.get('student_id')
        ).execute()



