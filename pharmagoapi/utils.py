import datetime
import time as stdlib_time

from django.conf import settings


def time() -> float:
    return stdlib_time.time()


def now(tz=None) -> datetime.datetime:
    t = time()
    return datetime.datetime.fromtimestamp(t, tz)


def now_us() -> int:
    return int(time() * 1_000_000)


def now_with_tz() -> datetime.datetime:
    return now(tz=datetime.timezone.utc)


def build_absolute_url(path: str) -> str:
    base_url = getattr(settings, "SITE_BASE_URL", None)
    base_url = base_url if base_url else "http://testserver"
    return f"{base_url}{path}"