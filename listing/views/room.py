from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from listing.models import Room
from listing.serializers import room as room_serializers
from listing.services import rooms_availability


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = room_serializers.RoomSerializer


class AvailableRoomsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = room_serializers.RoomAvailabilitySerializer(
            data={**request.query_params.dict(), "room_ids": request.query_params.getlist("room_ids")}
        )
        if not serializer.is_valid(raise_exception=True):
            return Response("query params are not valid", status=400)
        available_rooms_ids = rooms_availability.get_available_room_ids(**serializer.validated_data)
        return Response({"available room ids": available_rooms_ids}, status=status.HTTP_200_OK)
