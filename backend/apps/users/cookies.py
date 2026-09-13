"""Auth cookie helpers: one place for names, flags and lifetimes."""

from django.conf import settings

ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"

# Single source of truth: cookie lifetimes derive from token lifetimes.
ACCESS_MAX_AGE = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
REFRESH_MAX_AGE = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())

COOKIE_KWARGS = {
    "httponly": True,   # JS can't read it — the whole point of cookie-based JWT
    "samesite": "Lax",  # not sent on cross-site POSTs (CSRF guard)
    "secure": False,    # TODO: True in production (https only)
}


def set_access_cookie(response, access_token: str) -> None:
    response.set_cookie(ACCESS_COOKIE, access_token, max_age=ACCESS_MAX_AGE, **COOKIE_KWARGS)


def set_refresh_cookie(response, refresh_token: str) -> None:
    response.set_cookie(REFRESH_COOKIE, refresh_token, max_age=REFRESH_MAX_AGE, **COOKIE_KWARGS)


def clear_auth_cookies(response) -> None:
    response.delete_cookie(ACCESS_COOKIE)
    response.delete_cookie(REFRESH_COOKIE)
