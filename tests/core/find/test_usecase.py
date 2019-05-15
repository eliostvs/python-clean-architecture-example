import hypothesis.strategies as st
import pytest
from hypothesis import given

from example.core.shared.customer import CustomerCoordinate, Customer
from example.core.shared.geo import Distance, great_circle_distance
from example.core.find.usecase import find_nearest_customer
from tests.conftest import point_st


@pytest.fixture
def customer():
    return Customer(name="name", user_id=1)


@given(point_st)
def test_return_list_of_customers(customer, point):
    [customer] = find_nearest_customer(
        point, Distance.of(1), [CustomerCoordinate(customer, point)]
    )

    assert isinstance(customer, Customer)


@given(point_st, st.integers(min_value=10, max_value=100))
def test_returns_all_customers(customer, point, quantity):
    customer_coordinates = [
        CustomerCoordinate(customer, point) for _ in range(quantity)
    ]

    customers = find_nearest_customer(
        office_coordinate=point,
        max_distance_from_office=Distance.of(1),
        customer_coordinates=customer_coordinates,
    )

    assert quantity == len(customers)


@given(point_st, st.integers(min_value=10, max_value=100), st.text())
def test_returned_customer_are_sorted(point, integer, name):
    customer_coordinates = [
        CustomerCoordinate(Customer(name, integer), point) for _ in range(integer)
    ]

    customers = find_nearest_customer(
        office_coordinate=point,
        max_distance_from_office=Distance.of(1),
        customer_coordinates=customer_coordinates,
    )

    customers_id = [customer.user_id for customer in customers]

    assert sorted(customers_id) == customers_id


@given(
    st.tuples(point_st, point_st).filter(lambda t: t[0].longitude < t[1].longitude),
    st.integers(min_value=10, max_value=100),
)
def test_returns_none_customer(customer, points, integer):
    office_point, customer_point = points

    max_distance_from_office = Distance.of(
        great_circle_distance(office_point, customer_point).kilometers / 2
    )

    customer_coordinates = [
        CustomerCoordinate(customer, customer_point) for _ in range(integer)
    ]

    customers = find_nearest_customer(
        office_coordinate=office_point,
        max_distance_from_office=max_distance_from_office,
        customer_coordinates=customer_coordinates,
    )

    assert 0 == len(customers)
