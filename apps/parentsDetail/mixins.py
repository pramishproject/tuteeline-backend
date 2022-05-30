from apps.parentsDetail.usecases import GetParentsUseCase

class ParentsMixin:
    def get_parents(self):
        return GetParentsUseCase(
            parents_id = self.kwargs.get('parents_id')
        ).execute()