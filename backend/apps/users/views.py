import logging

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.cookies import (
    REFRESH_COOKIE,
    clear_auth_cookies,
    set_access_cookie,
    set_refresh_cookie,
)
from apps.users.models import User
from apps.users.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)


# Generic view: handles the whole "POST -> validate -> save -> 201" flow.
# We only plug in which serializer to use.
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


class UserDetailView(APIView):
    def get(self, request, pk):
        # get_object_or_404 = objects.get(pk=pk) + Http404 on DoesNotExist.
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# NOTE: generic equivalent of the view above — same behavior, 2 lines:
# class UserDetailView(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request):
        # 1. Validate the payload shape (email format, both fields present).
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Verify identity: hashes the given password and compares with the
        #    hash in DB. Returns a User or None. Never compare passwords manually.
        user = authenticate(
            request,
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            # Deliberately vague: don't reveal whether email exists or
            # the password is wrong (user enumeration protection).
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 3. Mint the token pair. Nothing is stored server-side:
        #    the tokens are self-contained (user_id + exp + signature).
        refresh = RefreshToken.for_user(user)

        # 4. User data in the body, tokens in httpOnly cookies.
        response = Response(UserSerializer(user).data)
        set_access_cookie(response, str(refresh.access_token))
        set_refresh_cookie(response, str(refresh))
        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]  # anonymous -> 401 before get() runs

    def get(self, request):
        # request.user is already set by CookieJWTAuthentication at this point.
        return Response(UserSerializer(request.user).data)


class RefreshView(APIView):
    def post(self, request):
        raw = request.COOKIES.get(REFRESH_COOKIE)
        if raw is None:
            return Response(
                {"detail": "No refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            # Parses + validates: signature, exp, token_type=refresh.
            refresh = RefreshToken(raw)
        except TokenError:
            return Response(
                {"detail": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Mint a fresh access from the same refresh token.
        response = Response({"detail": "ok"})
        set_access_cookie(response, str(refresh.access_token))
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        clear_auth_cookies(response)
        return response
