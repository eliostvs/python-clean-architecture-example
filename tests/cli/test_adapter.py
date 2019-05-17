from typing import List

import hypothesis.strategies as st
import pytest
import simplejson as json
from hypothesis import given

from example.cli.adapter import from_domain, schema, create_customer_coordinates
from example.core.domain.customer import Customer, CustomerCoordinate
from example.core.domain.exceptions import ValidationError
from example.core.domain.geo import Point
from tests.conftest import customer_name_st, user_id_st, longitude_st, latitude_st


@given(st.lists(st.builds(Customer, name=st.text())))
def test_from_domain(customers: List[Customer]):
    output = from_domain(customers)

    for customer in customers:
        assert f"{customer.user_id} - {customer.name}" in output


class TestCreateCustomerCoordinate:
    @given(customer_name_st, user_id_st, latitude_st, longitude_st)
    def test_successfully_returns_customer_coordinates(
        self, name, user_id, latitude, longitude
    ):
        marshal_result = schema.dump(
            dict(name=name, user_id=user_id, latitude=latitude, longitude=longitude)
        )

        assert marshal_result.errors == {}

        [customer_coordinate] = create_customer_coordinates(
            [json.dumps(marshal_result.data)]
        )

        assert isinstance(customer_coordinate, CustomerCoordinate)
        assert customer_coordinate.customer == Customer(name=name, user_id=user_id)
        assert customer_coordinate.coordinate == Point(
            latitude=latitude, longitude=longitude
        )

    @staticmethod
    def check_error_message(error_message: str, **kwargs):
        defaults = dict(name="name", user_id=1, latitude=1, longitude=1)
        marshal_result = schema.dump({**defaults, **kwargs})

        with pytest.raises(ValidationError) as error:
            create_customer_coordinates([json.dumps(marshal_result.data)])

        assert error_message in str(error.value)

    def test_raises_error_when_user_id_is_invalid(self):
        self.check_error_message(
            "Line 1 has 1 error(s). user_id: User id must be greater than 0.",
            user_id=-1,
        )

    def test_raises_error_when_latitude_is_invalid(self):
        self.check_error_message(
            "Line 1 has 1 error(s). latitude: Value must be less than 90 degrees.",
            latitude=91,
        )

    def test_raises_error_when_longitude_is_invalid(self):
        self.check_error_message(
            "Line 1 has 1 error(s). longitude: Value must be less than 180 degrees.",
            longitude=181,
        )

    def test_raises_error_when_user_name_is_invalid(self):
        self.check_error_message(
            "Line 1 has 1 error(s). name: Must not be empty", name=""
        )

    def test_raises_error_when_json_is_invalid(self):
        with pytest.raises(ValidationError) as error:
            create_customer_coordinates([""])

        assert "Invalid json" in str(error.value)
