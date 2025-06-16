import json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework.permissions import IsAuthenticated

from authentication.auth import CustomJWTAuthentication


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            refresh = data["refresh"]
            access = data["access"]

            response.set_cookie(
                key="access_token",
                value=access,
                httponly=True,
                secure=False,  # Set to True in prod (HTTPS)
                samesite="Lax",
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                secure=False,
                samesite="Lax",
            )
        return response


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response


class GetLoggedInUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
        }
        return Response(data)
