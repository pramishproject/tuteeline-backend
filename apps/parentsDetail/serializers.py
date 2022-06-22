import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core import fields
from apps.parentsDetail.models import StudentParents


class ParentsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentParents
        fields = (
            'relation',
            'fullname',
            'nationality',
            'occupation',
            'education',
            'annual_income',
            'currency',
            'email',
            'country_code',
            'contact',
        )

class UpdateParentsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentParents
        fields = (
            'relation',
            'fullname',
            'nationality',
            'occupation',
            'education',
            'annual_income',
            'currency',
            'email',
            'country_code',
            'contact',
        )



class GetParentsListSerializer(ParentsDetailSerializer):
    class Meta(ParentsDetailSerializer.Meta):
        fields = (
            'id',
            'relation',
            'fullname',
            'nationality',
            'occupation',
            'education',
            'annual_income',
            'currency',
            'email',
            'country_code',
            'contact',
        )  