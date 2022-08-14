from rest_framework import serializers

from apps.comment.models import ApplicationComments


class AppliocationCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ApplicationComments
        fields = (
            'user_id',
            'text_comment',
            'file_comment',
            'parent_comment',
        )

class ListChildCommentSerializer(serializers.ModelSerializer):
    user = serializers.DictField(source="user_data")
    class Meta:
        model = ApplicationComments
        fields = (
            'id',
            'user_id',
            'user',
            'text_comment',
            'file_comment',
            'parent_comment',
            'application',
            'created_at',
            'updated_at',
            # 'child_comment',
        )
class ListAppliocationCommentsSerializer(serializers.ModelSerializer):
    # child_comment = serializers.SerializerMethodField(method_name="count_child_comment")
    parent_application_comment = ListChildCommentSerializer(many=True)
    user = serializers.DictField(source="user_data")
    class Meta:
        model =  ApplicationComments
        fields = (
            'id',
            'user_id',
            'user',
            'text_comment',
            'file_comment',
            'parent_application_comment',
            'application',
            'created_at',
            'updated_at',
            # 'child_comment',
        )
    # def count_child_comment(self, obj):
    #     return ApplicationComments.objects.filter(parent_comment=obj.pk).count()