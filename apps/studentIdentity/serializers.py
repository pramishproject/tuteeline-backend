from django.db import models
from django.db.models import fields
from rest_framework import serializers

from apps.studentIdentity.models import Citizenship, Passport

class StudentCitizenshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizenship
        fields = (
            'citizenship_number',
            'issue_date',
            'issue_from',
            'front_page',
            'back_page'
        )

class UpdateCitizenshipFrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizenship
        fields = (
            'front_page',
        )

class UpdateCitizenshipBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizenship
        fields = (
            "back_page",
        )

class UpdateCitizenshipCharacterSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Citizenship
        fields = (
            'citizenship_number',
            'issue_date',
            'issue_from',
        )

class StudentPassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = (
            'passport_number',
            'issue_date',
            'expire_date',
            'issue_from',
            'passport_image'
        )

class StudentPassportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = (
            'passport_number',
            'issue_date',
            'expire_date',
            'issue_from',
        )
        
class PasswordImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = (
            'passport_image',
        )

class GetCitizenshipSerializer(StudentCitizenshipSerializer):
    class Meta(StudentCitizenshipSerializer.Meta):
        fields = '__all__'

class GetPassportSerializer(StudentPassportSerializer):
    class Meta(StudentPassportSerializer.Meta):
        fields = '__all__'