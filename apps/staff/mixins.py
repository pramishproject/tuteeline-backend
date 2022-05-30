from apps.staff.usecases import GetStaffPositionUseCase


class StaffPositionMixin:
    def get_staff_position(self):
        return GetStaffPositionUseCase(
            staff_position_id=self.kwargs.get('staff_position_id')
        ).execute()