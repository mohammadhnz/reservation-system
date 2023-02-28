from django.urls import path

from listing.views.report import RoomReportAPIView
from listing.views.reservation import ReservationViewSet
from listing.views.room import RoomViewSet, AvailableRoomsAPIView

room_create_list_view = RoomViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

room_update_retrieve_view = RoomViewSet.as_view(
    {
        "get": "retrieve",
        "patch": "partial_update",
    }
)

reservation_create_list_view = ReservationViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

reservation_update_retrieve_view = ReservationViewSet.as_view(
    {
        "get": "retrieve",
        "patch": "partial_update",
    }
)

urlpatterns = [
    path("rooms/", room_create_list_view),
    path("rooms/<int:pk>/", room_update_retrieve_view),
    path("rooms/available_rooms/", AvailableRoomsAPIView.as_view()),
    path("rooms/report/", RoomReportAPIView.as_view()),
    path("reservation/", room_update_retrieve_view),
    path("reservation/<int:pk>/", room_update_retrieve_view),
]
