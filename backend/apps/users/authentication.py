from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.cookies import ACCESS_COOKIE


class CookieJWTAuthentication(JWTAuthentication):
    """Reads the JWT from an httpOnly cookie instead of the Authorization header."""

    def authenticate(self, request):
        token = request.COOKIES.get(ACCESS_COOKIE)
        if token is None:
            return None  # no cookie -> not our case; request stays anonymous

        validated = self.get_validated_token(token)  # signature + exp check;
                                                     # raises AuthenticationFailed if bad
        return self.get_user(validated), validated   # SELECT user by user_id from payload
