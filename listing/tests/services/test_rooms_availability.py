from datetime import datetime

from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from parameterized import parameterized

from listing.services import rooms_availability
from listing.tests import model_factories


class TestRoomsAvailability(TestCase):
    @parameterized.expand(
        [
            (
                "WHEN_all_rooms_are_available",
                datetime(2022, 2, 8, tzinfo=timezone.utc),
                datetime(2021, 2, 10, tzinfo=timezone.utc),
                [100],
            )
        ]
    )
    @freeze_time(datetime(2022, 2, 3))
    def test_get_available_room_ids(self, _, check_in, check_out, expected):
        room = model_factories.RoomFactory(id=100)
        reservation = model_factories.ReservationFactory.create(
            check_in=datetime(2022, 2, 3), check_out=datetime(2022, 2, 6)
        )
        reservation.rooms.add(room)

        result = rooms_availability.get_available_room_ids([100], check_in, check_out)
        self.assertCountEqual(expected, result)
