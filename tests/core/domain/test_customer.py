import hypothesis.strategies as st
from hypothesis import given

from example.core.domain.customer import CustomerCoordinate, Customer
from example.core.domain.geo import Point


@given(st.text(), st.integers(), st.floats(), st.floats())
def test_customer_coordinate_factory(name, user_id, latitude, longitude):
    customer_coordinate = CustomerCoordinate.of(
        name=name, user_id=user_id, latitude=latitude, longitude=longitude
    )

    assert customer_coordinate.customer == Customer(name=name, user_id=user_id)
    assert customer_coordinate.coordinate == Point(
        latitude=latitude, longitude=longitude
    )
