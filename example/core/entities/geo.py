import math
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Point:
    latitude: Decimal
    longitude: Decimal

    @classmethod
    def of(cls, latitude: float, longitude: float) -> "Point":
        return cls(latitude=Decimal(latitude), longitude=Decimal(longitude))


@dataclass(order=True)
class Distance:
    kilometers: Decimal

    @classmethod
    def of(cls, kilometers: float) -> "Distance":
        return cls(kilometers=Decimal(kilometers))


EARTH_RADIUS_IN_KM = 6371.009


def great_circle_distance(point_a: Point, point_b: Point) -> Distance:
    """
    Calculates the distance between two points using the formula
    from https://en.wikipedia.org/wiki/Great-circle_distance
    It uses the constant `EARTH_RADIUS_IN_KM` as the great-circle radius.
    Example:
    >>> from example.core.geo import Point, great_circle_distance
    >>> rio_de_janeiro = Point.of(-22.9028, 43.2075)
    >>> sao_paulo = Point.of(-23.5475, 46.6361)
    >>> great_circle_distance(rio_de_janeiro, sao_paulo).kilometers
    >>> 357.5962
    """
    if point_a == point_b:
        return Distance.of(0)

    delta_longitude = point_b.longitude - point_a.longitude
    delta_radians = math.radians(delta_longitude)

    latitude_a_radians = math.radians(point_a.latitude)
    latitude_b_radians = math.radians(point_b.latitude)

    central_angle = math.acos(
        math.sin(latitude_a_radians) * math.sin(latitude_b_radians)
        + math.cos(latitude_a_radians)
        * math.cos(latitude_b_radians)
        * math.cos(delta_radians)
    )

    distance = EARTH_RADIUS_IN_KM * central_angle

    return Distance.of(distance)
