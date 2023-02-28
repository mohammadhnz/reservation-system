from rest_framework import serializers

from listing.models import Room, Reservation


class ReportParamsSerializer(serializers.Serializer):
    start = serializers.DateField()
    end = serializers.DateField()


class ReservationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("name", "check_in", "check_out")
        read_only_fields = ("name", "check_in", "check_out")


class RoomReportSerializer(serializers.ModelSerializer):
    reservations = ReservationReportSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ("id", "reservations")
