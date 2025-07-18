from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from authentication.views import CustomTokenObtainPairView, GetLoggedInUser, LogoutView


app_name = "auth"
urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("user", GetLoggedInUser.as_view(), name="user"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
