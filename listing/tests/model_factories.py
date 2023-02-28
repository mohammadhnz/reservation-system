import factory

from listing import models


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Room

    id = factory.Sequence(lambda n: n)
    beds_count = 2
    capacity = 2


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Reservation

    id = factory.Sequence(lambda n: n)
