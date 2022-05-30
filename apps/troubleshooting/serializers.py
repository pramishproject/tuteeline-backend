from rest_framework import serializers

from apps.troubleshooting.models import BillingTroubleshoot, Troubleshoot


class TroubleshootSerializer(serializers.ModelSerializer):
    class Meta:
        model = Troubleshoot
        fields = '__all__'


class AddTroubleshootTicketSerializer(TroubleshootSerializer):
    type = serializers.CharField(allow_blank=True)
    category = serializers.CharField(allow_blank=True)
    subject = serializers.CharField(allow_blank=True)

    class Meta(TroubleshootSerializer.Meta):
        fields = (
            'description',
            'troubleshoot_type',
            'type',
            'subject',
            'category'
        )


class ListTroubleShootTicketSerializer(TroubleshootSerializer):
    type = serializers.CharField(source='billingtroubleshoot.type')
    subject = serializers.CharField(source='billingtroubleshoot.subject')
    category = serializers.CharField(source='billingtroubleshoot.category')
    assigned_by = serializers.CharField(source='assigned_by.user.fullname',allow_null=True)
    assigned_to = serializers.CharField(source='assigned_to.user.fullname',allow_null=True)

    class Meta(TroubleshootSerializer.Meta):
        fields = (
            'id',
            'description',
            'assigned_by',
            'assigned_to',
            'troubleshoot_type',
            'type',
            'status',
            'subject',
            'category',

        )


class UpdateTravelshootSerializer(TroubleshootSerializer):
    class Meta(TroubleshootSerializer.Meta):
        fields =(
            'status',
            'assigned_to'

        )
