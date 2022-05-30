from rest_framework import serializers

from apps.schedule.models import CounsellingSchedule, Booking


class CounsellingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CounsellingSchedule


class AddCounsellingScheduleSerializer(CounsellingScheduleSerializer):
    class Meta(CounsellingScheduleSerializer.Meta):
        fields = (
            'title',
            'date',
            'start_time',
            'end_time',
            'location',
            'status'
        )


class ListCounsellingScheduleSerializer(CounsellingScheduleSerializer):
    counsellor = serializers.CharField()
    user = serializers.CharField(source='booking.user',allow_null=True)
    note = serializers.CharField(source='booking.note',allow_null=True)

    class Meta(CounsellingScheduleSerializer.Meta):
        fields = (
            'counsellor',
            'id',
            'title',
            'date',
            'start_time',
            'end_time',
            'location',
            'status',
            'user',
            'note'
        )


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Booking


class AddBookingSerializer(BookingSerializer):
    class Meta(BookingSerializer.Meta):
        fields = (
            'user',
            'note',
        )


class ListBookingSerializer(BookingSerializer):
    class Meta(BookingSerializer.Meta):
        fields = (
            'id',
            'is_booked',
            'created_at',
            'updated_at',
            'user',
            'note',
        )


class UpdateCounsellingScheduleSerializer(AddCounsellingScheduleSerializer):
    class Meta(AddCounsellingScheduleSerializer.Meta):
        fields = AddCounsellingScheduleSerializer.Meta.fields + (
            'counsellor',

        )

    # def validate_counsellor(self, attrs):
    #     if attrs.role == 'counsellor':
    #         return attrs
    #     return attrs


class UpdateBookingSerializer(BookingSerializer):
    class Meta(BookingSerializer.Meta):
        fields = (
            'schedule',
            'user',
            'note',
        )
