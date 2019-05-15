from decimal import Decimal

from hypothesis import given

from example.core.shared.geo import great_circle_distance, Point, Distance
from tests.conftest import point_st


@given(point_st, point_st)
def test_inverse_of_the_distances_is_equal(point_a, point_b):
    assert great_circle_distance(point_a, point_b) == great_circle_distance(
        point_b, point_a
    )


@given(point_st)
def test_distance_is_zero_point_is_equal(point):
    assert great_circle_distance(point, point) == Distance.of(0)


@given(point_st, point_st)
def test_returns_instance_of_point(a, b):
    distance = great_circle_distance(a, b)

    assert isinstance(distance, Distance)


def test_distance_between_sao_paulo_and_rio_de_janeiro_is_357_km():
    rio_de_janeiro = Point.of(-22.9028, 43.2075)
    sao_paulo = Point.of(-23.5475, 46.6361)

    assert round(
        great_circle_distance(rio_de_janeiro, sao_paulo).kilometers, 4
    ) == round(Decimal(357.5967), 4)
