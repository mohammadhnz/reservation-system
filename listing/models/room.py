from django.db import models

from core.models.base_model import HistoricalBaseModel


class Room(HistoricalBaseModel):
    beds_count = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
