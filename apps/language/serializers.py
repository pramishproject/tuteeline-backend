from apps.students import models
from django.db.models import fields
from rest_framework import serializers
from apps.language.models import Language
class CreateLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            'name' ,
            'first_language',
            'speak', 
            'read',
            'write',
            'spoken_at_home'
        )


class ListLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            'id',
            'name' ,
            'first_language',
            'speak', 
            'read',
            'write',
            'spoken_at_home'
        )