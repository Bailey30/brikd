from rest_framework import serializers

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


class CreateUserInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    name = serializers.CharField()
    search_postcode = serializers.CharField(required=False)
    search_location = serializers.CharField(required=False)


class UpdateUserInputSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    search_postcode = serializers.CharField(required=False)
    search_location = serializers.CharField(required=False)
