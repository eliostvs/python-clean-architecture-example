from dataclasses import dataclass
from decimal import Decimal

from .geo import Point


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
