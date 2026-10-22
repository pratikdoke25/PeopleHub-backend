from django.urls import path

from PeopleHub.apps.users.views import (
    LoginView,
    LogoutView,
    Profileview,
    RefreshView,
    Registerview,
)

app_name = "users"

urlpatterns = [
    path("register/", Registerview.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", Profileview.as_view(), name="profile"),
]