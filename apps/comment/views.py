from apps.comment.mixins import CommentMixins
from apps.comment.serializers import AppliocationCommentsSerializer, ListAppliocationCommentsSerializer
from apps.core import generics
from apps.institute_course.mixins import ApplyMixin
from apps.comment import usecases

class AddComment(generics.CreateWithMessageAPIView,ApplyMixin):
    serializer_class = AppliocationCommentsSerializer
    def get_object(self):
        return self.get_apply()

    def perform_create(self, serializer):
        return usecases.AddApplicationCommentUseCase(
            application=self.get_object(),
            serializer= serializer
        ).execute()
class ListApplicationComment(generics.ListAPIView,ApplyMixin):
    serializer_class = ListAppliocationCommentsSerializer

    def get_object(self):
        return self.get_apply()

    def get_queryset(self):
        return usecases.ListApplicationComment(
            application=self.get_object()
        ).execute()

class ListChildApplicationComment(generics.ListAPIView,CommentMixins):
    serializer_class = ListAppliocationCommentsSerializer

    def get_object(self):
        return self.get_comment()

    def get_queryset(self):
        return usecases.ListChildApplicationComment(
            comment=self.get_object()
        ).execute()