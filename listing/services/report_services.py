from datetime import datetime
from typing import List

from listing import repositoy as reservation_repository
from listing.models import Room


def get_rooms_reservation_by_time(start: datetime, end: datetime) -> List[Room]:
    rooms = reservation_repository.get_rooms_with_reservations_by_time(start, end)
    return [room for room in rooms if room.reservations.count() > 0]
