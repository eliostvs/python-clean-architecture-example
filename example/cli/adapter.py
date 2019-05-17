from decimal import Decimal
from json import JSONDecodeError
from typing import List, Dict

from marshmallow import (
    Schema,
    fields,
    post_load,
    ValidationError as MarshmallowValidationError,
    UnmarshalResult,
)

from example.core.domain.customer import CustomerCoordinate, Customer
from example.core.domain.exceptions import ValidationError


def _must_not_be_empty(value: str) -> None:
    if not value.strip():
        raise MarshmallowValidationError("Must not be empty")


def _must_be_positive(value: int) -> None:
    if value < 0:
        raise MarshmallowValidationError("User id must be greater than 0.")


def _must_be_less_than_180_degrees(value: Decimal) -> None:
    if abs(value) > 180:
        raise MarshmallowValidationError("Value must be less than 180 degrees.")


def _must_be_less_than_90_degrees(value: Decimal) -> None:
    if abs(value) > 90:
        raise MarshmallowValidationError("Value must be less than 90 degrees.")


class CustomerCoordinateSchema(Schema):
    name = fields.Str(required=True, validate=_must_not_be_empty)
    user_id = fields.Integer(required=True, validate=_must_be_positive)
    longitude = fields.Decimal(required=True, validate=_must_be_less_than_180_degrees)
    latitude = fields.Decimal(required=True, validate=_must_be_less_than_90_degrees)

    @post_load
    def make_customer_coordinate(self, data):
        return CustomerCoordinate.of(**data)


def from_domain(customers: List[Customer]) -> str:
    return "\n".join(
        [f"{customer.user_id} - {customer.name}" for customer in customers]
    )


schema = CustomerCoordinateSchema()


def create_customer_coordinates(lines: List[str]) -> List[CustomerCoordinate]:
    try:
        results = [schema.loads(line) for line in lines]
    except JSONDecodeError as error:
        raise ValidationError("Invalid json") from error
    else:
        _raise_validation_error_if_serializers_errors_were_found(results)

        return [each.data for each in results]


def _create_line_error(line_number: int, errors: Dict[str, List[str]]) -> str:
    field_errors = " ".join(
        f"{field}: {' '.join(values)}" for (field, values) in errors.items()
    )

    return f"Line {line_number} has {len(errors)} error(s). {field_errors}"


def _raise_validation_error_if_serializers_errors_were_found(
    results: List[UnmarshalResult]
) -> None:
    errors = [
        _create_line_error(index + 1, result.errors)
        for (index, result) in enumerate(results)
        if result.errors
    ]

    if errors:
        message = "\n".join(errors)
        raise ValidationError(message)
