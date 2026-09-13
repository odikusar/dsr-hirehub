# App-level routes. Mounted under /api/auth/ prefix in config/urls.py via include().
from django.urls import path

from apps.users.views import LoginView, LogoutView, MeView, RefreshView, RegisterView, UserDetailView

urlpatterns = [
    # .as_view() turns a class-based view into a callable the router expects.
    path("register/", RegisterView.as_view()),
    path("users/<int:pk>/", UserDetailView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", MeView.as_view()),
    path("refresh/", RefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
]
