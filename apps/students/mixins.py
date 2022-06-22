from apps.students.usecases import GetFavouriteByIdUseCase, GetStudentUseCase,GetAddressUseCase


class StudentMixin:
    def get_student(self):

        return GetStudentUseCase(student_id=self.kwargs.get('student_id')).execute()

class AddressMixin:
    def get_address(self):
        return GetAddressUseCase(address_id=self.kwargs.get('address_id')).execute()

class FavouriteMixin:
    def get_favourite(self):
        return GetFavouriteByIdUseCase(favourite_id=self.kwargs.get('favourite_id')).execute()