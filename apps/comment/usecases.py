from apps.comment.exceptions import CommentNotFound
from apps.comment.models import ApplicationComments
from apps.core.usecases import BaseUseCase
from apps.institute_course.models import InstituteApply


class GetCommentUseCase(BaseUseCase):
    def __init__(self,comment_id):
        self._comment_id = comment_id

    def execute(self):
        self._factory()
        return self._comment

    def _factory(self):
        try:
            self._comment=ApplicationComments.objects.get(
                pk = self._comment_id
            )
        except ApplicationComments.DoesNotExist:
            raise CommentNotFound

class AddApplicationCommentUseCase(BaseUseCase):
    def __init__(self , serializer ,application:InstituteApply):
        self._application= application
        self._serializer=serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self._comment = ApplicationComments.objects.create(
            **self._serializer,
            application=self._application
            )

class ListApplicationComment(BaseUseCase):
    def __init__(self,application):
        self._application = application

    def execute(self):
        self._factory()
        return self._comment
    def _factory(self):
        self._comment = ApplicationComments.objects.filter(
            application=self._application,
            parent_comment=None,
            # user_id__user_type ="institute_user"
        ).prefetch_related('parent_application_comment').order_by('created_at')[:: -1]

class ListChildApplicationComment(BaseUseCase):
    def __init__(self,comment):
        self._comment = comment

    def execute(self):
        self._factory()
        return self._child_comment
    def _factory(self):
        self._child_comment = ApplicationComments.objects.filter(
            parent_comment=self._comment,
        ).order_by('created_at')