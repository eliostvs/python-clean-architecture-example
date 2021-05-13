from hypothesis import given, strategies as st

from example.search import search_nearest_customers
from example.search.customer import Customer, CustomerCoordinate
from example.search.geo import Distance, Point, great_circle_distance
from tests.conftest import name_st, point_st


@given(st.text(), st.integers(), st.floats(), st.floats())
def test_customer_coordinate_factory(name, user_id, latitude, longitude):
    customer_coordinate = CustomerCoordinate.of(
        name=name, user_id=user_id, latitude=latitude, longitude=longitude
    )

    assert customer_coordinate.customer == Customer(name=name, user_id=user_id)
    assert customer_coordinate.coordinate == Point(
        latitude=latitude, longitude=longitude
    )


@given(point_st, st.integers(min_value=10, max_value=100))
def test_find_customers_near_the_office(point, quantity):
    customer = Customer(name="name", user_id=1)
    customer_coordinates = [
        CustomerCoordinate(customer, point) for _ in range(quantity)
    ]

    found_customers = search_nearest_customers(
        origin=point,
        max_distance=Distance.of(1),
        customers=customer_coordinates,
    )

    assert len(found_customers) == quantity


@given(point_st, st.integers(min_value=10, max_value=100), name_st)
def test_customer_are_sorted(point, quantity, name):
    customer_coordinates = [
        CustomerCoordinate(Customer(name, quantity), point) for _ in range(quantity)
    ]

    customers = search_nearest_customers(
        origin=point,
        max_distance=Distance.of(1),
        customers=customer_coordinates,
    )

    customers_id = [customer.user_id for customer in customers]

    assert customers_id == sorted(customers_id)


@given(
    # the second point should have a bigger longitude
    st.tuples(point_st, point_st).filter(lambda t: t[0].longitude * 2 < t[1].longitude),
    st.integers(min_value=10, max_value=100),
)
def test_returns_none_customer(points, quantity):
    point_a, point_b = points

    # the max distance is half the distance between the two points
    kilometers = great_circle_distance(point_a, point_b).kilometers / 2
    customer = Customer(name="name", user_id=1)
    customer_coordinates = [
        CustomerCoordinate(customer, point_b) for _ in range(quantity)
    ]

    customers = search_nearest_customers(
        origin=point_a,
        max_distance=Distance(kilometers),
        customers=customer_coordinates,
    )

    assert len(customers) == 0
