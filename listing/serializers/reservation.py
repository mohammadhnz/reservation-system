from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from listing import repositoy as reservation_repository
from listing.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    rooms = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ("id", "name", "check_in", "check_out", "rooms")
        read_only_fields = ("id", "name", "check_in", "check_out", "rooms")

    def get_rooms(self, reservation):
        return reservation.rooms.all().values_list("id", flat=True)


class ReservationCreateUpdateSerializer(serializers.ModelSerializer):
    room_ids = serializers.ListSerializer(write_only=True, child=serializers.IntegerField())

    class Meta:
        model = Reservation
        fields = (
            "name",
            "room_ids",
            "check_in",
            "check_out",
            "status",
        )

    def validate(self, attrs):
        room_ids = attrs.get("room_ids")
        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")

        reservations = reservation_repository.get_rooms_reservations_in_time_range(room_ids, check_in, check_out)

        if self.instance and reservations.exclude(id=self.instance.id).count() > 0:
            raise ValidationError("all rooms are not available.")
        elif self.instance is None and reservations.count() > 0:
            raise ValidationError("all rooms are not available.")

        return super().validate(attrs)

    def create(self, validated_data):
        with transaction.atomic():
            room_ids = validated_data.pop("room_ids", [])
            rooms = reservation_repository.get_rooms_by_id(room_ids)

            reservation = super().create(validated_data)

            reservation.rooms.set(rooms)

            return reservation

    def update(self, instance, validated_data):
        with transaction.atomic():
            room_ids = validated_data.pop("room_ids", [])
            rooms = reservation_repository.get_rooms_by_id(room_ids)

            reservation = super().update(instance, validated_data)

            reservation.rooms.set(rooms)

            return reservation
