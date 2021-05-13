from decimal import getcontext
from typing import TextIO

import click
from pydantic import ValidationError

from example.config import DEFAULTS
from example.search import Distance, Point, search_nearest_customers
from .input import create_customer_coordinates, stringify_customers

getcontext().prec = 7


@click.command()
@click.argument("file_stream", type=click.File("r"))
@click.option(
    "--max-distance",
    default=DEFAULTS["distance_in_km"],
    type=float,
    help="max distance from office in kilometers",
)
@click.option(
    "--office-latitude",
    default=DEFAULTS["office_latitude"],
    type=float,
    help="office decimal latitude",
)
@click.option(
    "--office-longitude",
    default=DEFAULTS["office_longitude"],
    type=float,
    help="office decimal longitude",
)
def main(
    file_stream: TextIO,
    max_distance: float,
    office_latitude: float,
    office_longitude: float,
) -> None:
    """
    Finds the nearest customers from the office.
    """
    try:
        sorted_customers_nearby = search_nearest_customers(
            origin=Point.of(latitude=office_latitude, longitude=office_longitude),
            max_distance=Distance.of(max_distance),
            customers=create_customer_coordinates(file_stream.readlines()),
        )
    except ValidationError as error:
        click.echo(error)
    else:
        click.echo(stringify_customers(sorted_customers_nearby))
