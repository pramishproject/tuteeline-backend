from apps.comment import usecases
class CommentMixins:
    def get_comment(self):
        return usecases.GetCommentUseCase(
            comment_id=self.kwargs.get("comment_id")
        ).execute()