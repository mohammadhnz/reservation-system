from datetime import datetime

from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from parameterized import parameterized

from listing import repositoy
from listing.models import Reservation
from listing.tests import model_factories


class TestRepository(TestCase):
    def setUp(self) -> None:
        self.reservation = model_factories.ReservationFactory.create(
            check_in=datetime(2022, 2, 3), check_out=datetime(2022, 2, 6)
        )

    def test_get_rooms_by_id(self):
        for i in range(3):
            model_factories.RoomFactory.create(id=i)
        result = repositoy.get_rooms_by_id([0, 1, 2]).values_list("id", flat=True)
        expected = [0, 1, 2]
        self.assertCountEqual(expected, result)

    @parameterized.expand(
        [
            (
                "WHEN_there_is_no_reservation",
                datetime(2022, 2, 8, tzinfo=timezone.utc),
                datetime(2022, 2, 10, tzinfo=timezone.utc),
                0,
            ),
            (
                "WHEN_reservation_exists_with_same_check_in_as_check_out",
                datetime(2022, 2, 6, tzinfo=timezone.utc),
                datetime(2022, 2, 9, tzinfo=timezone.utc),
                0,
            ),
            (
                "WHEN_reservation_exists_with_same_check_out_as_check_in",
                datetime(2022, 2, 1, tzinfo=timezone.utc),
                datetime(2022, 2, 3, tzinfo=timezone.utc),
                0,
            ),
            (
                "WHEN_reservation_exists",
                datetime(2022, 2, 3, tzinfo=timezone.utc),
                datetime(2022, 2, 4, tzinfo=timezone.utc),
                1,
            ),
        ]
    )
    @freeze_time(datetime(2022, 2, 3))
    def test__filter_with_time(self, _, check_in, check_out, expected_count):
        self.assertEqual(
            expected_count, repositoy._filter_with_time(Reservation.objects.all(), check_in, check_out).count()
        )

    @parameterized.expand(
        [
            (
                "WHEN_there_is_no_reservation",
                datetime(2022, 2, 8, tzinfo=timezone.utc),
                datetime(2022, 2, 10, tzinfo=timezone.utc),
                0,
            ),
            (
                "WHEN_reservation_exists",
                datetime(2022, 2, 3, tzinfo=timezone.utc),
                datetime(2022, 2, 4, tzinfo=timezone.utc),
                1,
            ),
        ]
    )
    @freeze_time(datetime(2022, 2, 3))
    def test_get_reservations_by_room_id(self, _, check_in, check_out, expected_count):
        room = model_factories.RoomFactory.create()
        self.reservation.rooms.add(room)

        self.assertEqual(expected_count, repositoy.get_reservations_by_room_id([room.id], check_in, check_out).count())

    @freeze_time(datetime(2022, 2, 3))
    def test_get_rooms_with_reservations_by_room_ids(self):

        room = model_factories.RoomFactory.create()
        self.reservation.rooms.add(room)
        result = repositoy.get_rooms_with_reservations_by_room_ids(
            [room.id], datetime(2022, 2, 3), datetime(2022, 2, 4)
        )
        self.assertEqual(1, result.count())
        self.assertEqual(1, result.first().reservations.count())
        self.assertEqual(self.reservation, result.first().reservations.first())
