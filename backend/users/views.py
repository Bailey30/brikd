from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from users.services import UserService
from common.models import BaseUserSerializer
from users.models import User


class UserOutputSerializer(serializers.ModelSerializer):
    profile = BaseUserSerializer()

    class Meta:  # pyright: ignore
        model = User
        fields = [
            "id",
            "name",
            "profile",
            "search_postcode",
            "search_location",
        ]
        depth = 1


class CreateUserView(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
        name = serializers.CharField()
        search_postcode = serializers.CharField(required=False)
        search_location = serializers.CharField(required=False)

    def post(self, request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService().create(**serializer.validated_data)

        return Response(
            data={
                "user": UserOutputSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )
