from django.db import models
from django.db.models import fields
from rest_framework import serializers

from apps.blog.models import Blogs, InstituteBlog, Relation, PortalBlog, ConsultancyBlog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = '__all__'


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'


class AddBlogSerializer(BlogSerializer):
    class Meta(BlogSerializer.Meta):
        fields = (
            'title',
            'relation',
            'image',
            'content',
            'author_name',
        )


class ListBlogSerializer(BlogSerializer):
    class Meta(BlogSerializer.Meta):
        fields = (
            'id',
            'title',
            'relation',
            'image',
            'content',
            'author_name',
            'created_at',
            'updated_at',
        )


class UpdateBlogSerializer(AddBlogSerializer):
    pass


class AddRelationSerializer(RelationSerializer):
    class Meta(RelationSerializer.Meta):
        fields = (
            'name',
        )


class ListRelationSerializer(RelationSerializer):
    class Meta(RelationSerializer.Meta):
        fields = (
            'id',
            'name',
            'created_at',
            'updated_at',
        )



class UpdateRelationSerialzier(AddRelationSerializer):
    pass


class CreateInstituteBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteBlog
        fields = (
            'relation',
            'title',
            'author_name',
            'content',
            'image',
        )

class ListInstituteBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteBlog
        fields = "__all__"

class UpdateInstituteBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteBlog
        fields = (
            'relation',
            'title',
            'author_name',
            'content',
            'image',
        )

class CreatePortalUserBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortalBlog
        fields = (
            'title',
            'author_name',
            'content',
            'image',
        )

# --------------------------Consultancy Serializer------------------
class CreateConsultancyBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyBlog
        fields = (
            'title',
            'relation',
            'content',
            'consultancy',
            'image',
            'author_name',
        )

class UpdateConsultancyBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyBlog
        fields = (
            'title',
            'relation',
            'content',
            'image',
            'author_name',
        )

class ApproveConsultancyBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyBlog
        fields = (
            'verified',
        )
class ListConsultancyBlogForStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyBlog
        fields = (
            'title',
            'relation',
            'content',
            'consultancy',
            'image',
            'author_name',
            'created_at'
        )

class ListConsultancyBlog(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyBlog
        fields = "__all__"


# ---------------------------END Consultancy Serializer-------------