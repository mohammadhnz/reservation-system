from rest_framework import viewsets

from listing.models import Reservation
from listing.serializers import reservation as reservation_serializers


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return reservation_serializers.ReservationCreateUpdateSerializer
        return reservation_serializers.ReservationSerializer
