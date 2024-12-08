from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (BlockUsersView, UserCreateView, UserDetailView,
                         UserForgotPasswordView, UserListView,
                         UserPasswordResetConfirmView, UserUpdateView)

app_name = UsersConfig.name

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="login.html", next_page="messaging:main"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="messaging:main"), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("password-reset/", UserForgotPasswordView.as_view(), name="password_reset"),
    path(
        "set-new-password/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user/<int:pk>/block", BlockUsersView.as_view(), name="user_block"),
]
