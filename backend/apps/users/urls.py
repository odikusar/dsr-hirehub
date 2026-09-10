# App-level routes. Mounted under /api/auth/ prefix in config/urls.py via include().
from django.urls import path

from apps.users.views import RegisterView, UserDetailView

urlpatterns = [
    # .as_view() turns a class-based view into a callable the router expects.
    path("register/", RegisterView.as_view()),
    path("users/<int:pk>/", UserDetailView.as_view()),
]
