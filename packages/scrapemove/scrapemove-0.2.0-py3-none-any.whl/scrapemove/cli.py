"""Console script for scrapemove."""

import logging
import sys

import click

from scrapemove.scrapemove import search as search_internal, details as details_internal


@click.group()
def main():
    """Console script for scrapemove."""
    logging.basicConfig(level=logging.INFO)
    return 0


@main.command()
@click.argument("url")
@click.option("--parallelism", type=int)
@click.option("--details/--no-details", default=False)
@click.option(
    "--rate-limit",
    type=int,
    default=1000,
    help="Number of requests per second to rate limit to",
)
def search(url, parallelism, details, rate_limit):
    """Search for properties."""
    click.echo(
        search_internal(
            url,
            detailed=details,
            rate_limit_per_sec=rate_limit,
            parallelism=parallelism,
        )
    )
    return 0


@main.command()
@click.argument("url")
def details(url):
    """Fetch details for a property."""
    click.echo(details_internal([url]))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
