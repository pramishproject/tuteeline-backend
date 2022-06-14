from apps.blog.usecases import GetBlogsUseCase, GetInstituteBlogsByIdUseCase, \
    GetPortalBlogByIdUseCase, GetRelationUseCase,GetConsultancyUseCase


class BlogsMixin:
    def get_blogs(self):
        return GetBlogsUseCase(
            blog_id=self.kwargs.get('blog_id')
        ).execute()


class RelationMixin:
    def get_relation(self):
        return GetRelationUseCase(
            relation_id=self.kwargs.get('relation_id')
        ).execute()

class InstituteBlogMixin:
    def get_institute_blog(self):
        return GetInstituteBlogsByIdUseCase(
            institute_blog_id=self.kwargs.get('institute_blog_id')
        ).execute()

class ConsultancyBlogMixin:
    def get_consultancy_blog(self):
        return GetConsultancyUseCase(
            consultancy_blog_id=self.kwargs.get('consultancy_blog_id')
        ).execute()