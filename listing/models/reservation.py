from django.db import models

from core.models.base_model import HistoricalBaseModel
from listing.models.room import Room
from model_utils import Choices


class Reservation(HistoricalBaseModel):
    ReservationStatus = Choices(
        ("ACTIVE", "ACTIVE"),
        ("CANCELED", "CANCELED"),
    )
    name = models.CharField(max_length=256)
    rooms = models.ManyToManyField(to=Room, related_name="reservations")
    check_in = models.DateField(null=False)
    check_out = models.DateField(null=False)
    status = models.CharField(max_length=30, choices=ReservationStatus, default=ReservationStatus.ACTIVE)
