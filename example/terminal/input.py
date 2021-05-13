from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field, validator

from example.search import Customer, CustomerCoordinate


class CustomerCoordinateInput(BaseModel):
    name: str = Field(min_length=2)
    user_id: int = Field(ge=1)
    longitude: Decimal
    latitude: Decimal

    @validator("longitude")
    def longitude_must_be_less_than_180_degrees(cls, value):
        if abs(value) > 180:
            raise ValueError("value must be less than 180 degrees.")
        return value

    @validator("latitude")
    def latitude_must_be_less_than_90_degrees(cls, value):
        if abs(value) > 90:
            raise ValueError("value must be less than 90 degrees.")
        return value

    def to_domain(self):
        return CustomerCoordinate.of(**self.dict())


def stringify_customers(customers: List[Customer]) -> str:
    return "\n".join(
        [f"{customer.user_id} - {customer.name}" for customer in customers]
    )


def create_customer_coordinates(lines: List[str]) -> List[CustomerCoordinate]:
    return [CustomerCoordinateInput.parse_raw(line).to_domain() for line in lines]
