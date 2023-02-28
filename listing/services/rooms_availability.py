from datetime import datetime
from typing import List

from listing import repositoy as reservation_repository


def get_available_room_ids(room_ids: List[int], check_in: datetime, check_out: datetime) -> List[int]:
    rooms = reservation_repository.get_rooms_with_reservations_by_room_ids(room_ids, check_in, check_out)
    return [room.id for room in rooms if room.reservations.count() == 0]
