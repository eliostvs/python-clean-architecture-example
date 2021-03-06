from operator import attrgetter
from typing import List

from example.core.customer import Customer, CustomerCoordinate
from example.core.geo import Point, Distance, great_circle_distance


def nearest_customer(
    office_coordinate: Point,
    max_distance_from_office: Distance,
    customer_coordinates: List[CustomerCoordinate],
) -> List[Customer]:
    return sorted(
        [
            each.customer
            for each in customer_coordinates
            if great_circle_distance(office_coordinate, each.coordinate)
            <= max_distance_from_office
        ],
        key=attrgetter("user_id"),
    )
