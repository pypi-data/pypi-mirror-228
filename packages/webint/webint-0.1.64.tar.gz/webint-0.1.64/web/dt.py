import pendulum

__all__ = ["parse_dt", "now"]


def parse_dt(dt: str, **options) -> pendulum.DateTime:
    """Parse `dt` and return a datetime object."""
    return pendulum.parser.parse(dt, **options)


def now() -> pendulum.DateTime:
    """Return the current datetime."""
    return pendulum.now("UTC")
