import re
from turtle import mode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from apps.core import fields

from apps.academic.models import Academic, PersonalEssay, StudentLor, StudentSop

class CreateAcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic
        fields = (
            'institute_name',
            'duration',
            'level',
            'score',
            'full_score',
            'marksheet',
            'certificate'
        )


class GetAcademicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic
        fields = (
            'id',
            'institute_name',
            'duration',
            'level',
            'score',
            'full_score',
            'marksheet',
            'certificate'
        )

class UpdateAcademicSerializer(GetAcademicListSerializer):
    class Meta(GetAcademicListSerializer.Meta):
        fields = (
            'institute_name',
            'duration',
            'level',
            'score',
            'full_score',
        )

class UpdateCertificateSerializer(GetAcademicListSerializer):
    class Meta(GetAcademicListSerializer.Meta):
        fields = (
            'certificate',
        )

class UpdateMarksheetSerializer(GetAcademicListSerializer):
    class Meta(GetAcademicListSerializer.Meta):
        fields = (
            'marksheet',
        )

class CreateSopSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSop
        fields = (
            'document',
            'name',
        )


class CreateLorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLor
        fields = (
            'document',
            'name'
        )

class CreateEssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalEssay
        fields = (
            'essay',
            'name',
            'content'
        )

class GetLorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLor
        fields = '__all__'

class GetPersonalEssay(serializers.ModelSerializer):
    class Meta:
        model = PersonalEssay
        fields = '__all__'

class GetSopSerializer(CreateSopSerializer):
    class Meta(CreateSopSerializer.Meta):
        fields = '__all__'

class UpdateSopSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSop
        fields = (
            'document',
            'name',
        )

class UpdateEssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalEssay
        fields = (
            'essay',
            'name',
            'content',
        )

