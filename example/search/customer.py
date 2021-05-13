from dataclasses import dataclass
from decimal import Decimal
from operator import attrgetter
from typing import List

from .geo import Distance, Point, great_circle_distance


@dataclass
class Customer:
    name: str
    user_id: int


@dataclass
class CustomerCoordinate:
    customer: Customer
    coordinate: Point

    @classmethod
    def of(
        cls, name: str, user_id: int, latitude: Decimal, longitude: Decimal
    ) -> "CustomerCoordinate":
        return cls(
            customer=Customer(name=name, user_id=user_id),
            coordinate=Point(latitude=latitude, longitude=longitude),
        )


def search_nearest_customers(
    origin: Point,
    max_distance: Distance,
    customers: List[CustomerCoordinate],
) -> List[Customer]:
    """
    Use case.
    Search the customers that are near a given point than sort them by id.
    """
    return sorted(
        [
            each.customer
            for each in customers
            if great_circle_distance(origin, each.coordinate) <= max_distance
        ],
        key=attrgetter("user_id"),
    )
