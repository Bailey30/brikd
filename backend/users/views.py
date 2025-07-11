from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from authentication.views import BaseAuthenticatedView
from users.serializers import (
    CreateUserInputSerializer,
    UpdateUserInputSerializer,
    UserOutputSerializer,
)
from users.services import UserService
from users.models import User
from users.swagger import create_user_view_schema, update_user_view_schema


class CreateUserView(CreateAPIView):
    @swagger_auto_schema(**create_user_view_schema)
    def post(self, request) -> Response:
        serializer = CreateUserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService().create(**serializer.validated_data)

        return Response(
            data={
                "user": UserOutputSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class UpdateUserView(BaseAuthenticatedView):
    @swagger_auto_schema(**update_user_view_schema)
    def patch(self, request, id) -> Response:
        serializer = UpdateUserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = UserService().get(id)
            updated_user = UserService().update(user, serializer.validated_data)
        except User.DoesNotExist:
            raise NotFound(detail="User with this ID does not exist.")

        return Response(
            data={"user": UserOutputSerializer(updated_user).data},
            status=status.HTTP_200_OK,
        )
