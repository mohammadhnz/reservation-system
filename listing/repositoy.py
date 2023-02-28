from datetime import datetime
from typing import List

from django.db.models import QuerySet, Q, Prefetch

from listing.models import Room, Reservation


def get_rooms_by_id(ids: List[int]) -> QuerySet[Room]:
    return Room.objects.filter(id__in=ids)


def get_rooms_reservations_in_time_range(
    room_ids: List[int], check_in: datetime, check_out: datetime
) -> QuerySet[Reservation]:
    return _filter_with_time(Reservation.objects.filter(rooms__in=get_rooms_by_id(room_ids)), check_in, check_out)


def get_rooms_with_reservations_in_time_range(
    room_ids: List[int], check_in: datetime, check_out: datetime
) -> QuerySet[Room]:
    return get_rooms_by_id(room_ids).prefetch_related(
        Prefetch("reservations", queryset=_filter_with_time(Reservation.objects.all(), check_in, check_out))
    )


def _filter_with_time(reservations: QuerySet[Reservation], check_in: datetime, check_out: datetime):
    return reservations.filter(
        Q(check_in__lte=check_in, check_out__gt=check_in)
        | Q(check_in__lt=check_out, check_out__gte=check_out)
        | Q(check_in__gte=check_in, check_out__lte=check_out)
    )
