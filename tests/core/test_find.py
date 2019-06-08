import hypothesis.strategies as st
import pytest
from hypothesis import given

from example.core.customer import CustomerCoordinate, Customer
from example.core.find import nearest_customer
from example.core.geo import Distance, great_circle_distance
from tests.conftest import point_st, name_st


@pytest.fixture
def customer():
    return Customer(name="name", user_id=1)


@given(point_st, st.integers(min_value=10, max_value=100))
def test_find_customers_near_the_office(customer, point, quantity):
    customer_coordinates = [
        CustomerCoordinate(customer, point) for _ in range(quantity)
    ]

    found_customers = nearest_customer(
        office_coordinate=point,
        max_distance_from_office=Distance.of(1),
        customer_coordinates=customer_coordinates,
    )

    assert len(found_customers) == quantity


@given(point_st, st.integers(min_value=10, max_value=100), name_st)
def test_customer_are_sorted(point, quantity, name):
    customer_coordinates = [
        CustomerCoordinate(Customer(name, quantity), point) for _ in range(quantity)
    ]

    customers = nearest_customer(
        office_coordinate=point,
        max_distance_from_office=Distance.of(1),
        customer_coordinates=customer_coordinates,
    )

    customers_id = [customer.user_id for customer in customers]

    assert customers_id == sorted(customers_id)


@given(
    # the second point should have a bigger longitude
    st.tuples(point_st, point_st).filter(lambda t: t[0].longitude * 2 < t[1].longitude),
    st.integers(min_value=10, max_value=100),
)
def test_returns_none_customer(customer, points, quantity):
    office_point, customer_point = points

    # the max distance is half the distance between the two points
    max_distance_from_office = Distance.of(
        great_circle_distance(office_point, customer_point).kilometers / 2
    )

    customer_coordinates = [
        CustomerCoordinate(customer, customer_point) for _ in range(quantity)
    ]

    customers = nearest_customer(
        office_coordinate=office_point,
        max_distance_from_office=max_distance_from_office,
        customer_coordinates=customer_coordinates,
    )

    assert len(customers) == 0
