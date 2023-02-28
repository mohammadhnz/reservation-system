from datetime import datetime

from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from parameterized import parameterized

from listing.services import report_services
from listing.tests import model_factories


class TestReport(TestCase):
    @parameterized.expand(
        [
            (
                "WHEN_there_is_no_reservations",
                datetime(2022, 2, 8, tzinfo=timezone.utc),
                datetime(2022, 2, 25, tzinfo=timezone.utc),
                0,
            ),
            (
                "WHEN_reservation_exists_in_time_range",
                datetime(2022, 2, 1, tzinfo=timezone.utc),
                datetime(2022, 2, 25, tzinfo=timezone.utc),
                1,
            ),
        ]
    )
    @freeze_time(datetime(2022, 2, 3))
    def test_get_rooms_reservation_by_time(self, _, start, end, expected):
        room = model_factories.RoomFactory(id=100)
        reservation = model_factories.ReservationFactory.create(
            check_in=datetime(2022, 2, 3), check_out=datetime(2022, 2, 6)
        )
        reservation.rooms.add(room)

        result = report_services.get_rooms_reservation_by_time(start, end)
        self.assertEqual(expected, len(result))
