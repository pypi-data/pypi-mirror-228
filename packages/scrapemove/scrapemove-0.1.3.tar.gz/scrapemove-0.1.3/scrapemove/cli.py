"""Console script for scrapemove."""

import logging
import sys

import click

from scrapemove.scrapemove import request


@click.command()
@click.argument("url")
@click.option("--parallelism", type=int)
@click.option("--details/--no-details", default=False)
@click.option(
    "--rate-limit",
    type=int,
    default=1000,
    help="Number of requests per second to rate limit to",
)
def main(url, parallelism, details, rate_limit):
    """Console script for scrapemove."""
    logging.basicConfig(level=logging.INFO)
    click.echo(
        request(
            url,
            detailed=details,
            rate_limit_per_sec=rate_limit,
            parallelism=parallelism,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
