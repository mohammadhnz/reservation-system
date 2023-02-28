from rest_framework import serializers

from listing.models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class RoomAvailabilitySerializer(serializers.Serializer):
    room_ids = serializers.ListField(child=serializers.IntegerField(min_value=0), allow_empty=False, allow_null=False)
    check_in = serializers.DateField()
    check_out = serializers.DateField()
