from decimal import Decimal

from hypothesis import given

from example.search.geo import Distance, Point, great_circle_distance
from tests.conftest import point_st


@given(point_st, point_st)
def test_distance_is_symmetric(point_a, point_b):
    assert great_circle_distance(point_a, point_b) == great_circle_distance(
        point_b, point_a
    )


@given(point_st)
def test_distance_is_zero_when_the_points_are_equal(point):
    assert great_circle_distance(point, point) == Distance.of(0)


def test_distance_between_two_cities():
    rio_de_janeiro = Point.of(-22.9028, 43.2075)
    sao_paulo = Point.of(-23.5475, 46.6361)

    assert round(
        great_circle_distance(rio_de_janeiro, sao_paulo).kilometers, 4
    ) == round(Decimal(357.5967), 4)
