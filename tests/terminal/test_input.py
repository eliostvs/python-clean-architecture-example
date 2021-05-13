import json
from typing import List

import hypothesis.strategies as st
import pytest
from hypothesis import given
from pydantic import ValidationError

from example.search import Customer, CustomerCoordinate, Point
from example.terminal.input import (
    CustomerCoordinateInput,
    create_customer_coordinates,
    stringify_customers,
)
from tests.conftest import latitude_st, longitude_st, name_st, user_id_st


@given(st.lists(st.builds(Customer, name=st.text())))
def test_stringify_customers(customers: List[Customer]):
    output = stringify_customers(customers)

    for customer in customers:
        assert f"{customer.user_id} - {customer.name}" in output


class TestCreateCustomerCoordinate:
    @given(name_st, user_id_st, latitude_st, longitude_st)
    def test_successfully_returns_customer_coordinates(
        self, name, user_id, latitude, longitude
    ):
        customer_coordinate_input = CustomerCoordinateInput.parse_obj(
            dict(
                name=name,
                user_id=user_id,
                latitude=latitude,
                longitude=longitude,
            )
        )

        [customer_coordinate] = create_customer_coordinates(
            [customer_coordinate_input.json()]
        )

        assert isinstance(customer_coordinate, CustomerCoordinate)
        assert customer_coordinate.customer == Customer(name=name, user_id=user_id)
        assert customer_coordinate.coordinate == Point(
            latitude=latitude, longitude=longitude
        )

    def test_raises_error_when_user_id_is_invalid(self):
        self.check_error_message(
            "user_id\n  ensure this value is greater than or equal to 1",
            user_id=-1,
        )

    def test_raises_error_when_latitude_is_invalid(self):
        self.check_error_message(
            "latitude\n  value must be less than 90 degrees.",
            latitude=91,
        )

    def test_raises_error_when_longitude_is_invalid(self):
        self.check_error_message(
            "longitude\n  value must be less than 180 degrees.",
            longitude=181,
        )

    def test_raises_error_when_user_name_is_invalid(self):
        self.check_error_message(
            "name\n  ensure this value has at least 2 characters", name=""
        )

    @staticmethod
    def check_error_message(message: str, **kwargs):
        defaults = dict(name="name", user_id=1, latitude=1, longitude=1)

        with pytest.raises(ValidationError) as error:
            create_customer_coordinates([json.dumps({**defaults, **kwargs})])

        assert "1 validation error for CustomerCoordinateInput" in str(error.value)
        assert message in str(error.value)
