import pendulum
import pendulum.datetime

__all__ = ["parse_dt", "now"]


def parse_dt(dt: str, **options) -> pendulum.datetime.DateTime:
    """Parse `dt` and return a datetime object."""
    return pendulum.parser.parse(dt, **options)


def now() -> pendulum.datetime.DateTime:
    """Return the current datetime."""
    return pendulum.now("UTC")
