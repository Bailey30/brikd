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
            "phone_number",
            "distance_alerts",
            "alert_radius",
            "search_postcode_coordinates",
        ]
        depth = 1

    def to_representation(self, model):  # pyright: ignore
        values = super().to_representation(model)
        values["search_postcode_coordinates"] = {
            "longitude": model.search_postcode_coordinates[0],
            "latitude": model.search_postcode_coordinates[1],
        }
        return values


class CreateUserInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    name = serializers.CharField()
    search_postcode = serializers.CharField(required=False)
    search_location = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    distance_alerts = serializers.BooleanField(required=False)
    alert_radius = serializers.IntegerField(required=False)


class UpdateUserInputSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    search_postcode = serializers.CharField(required=False)
    search_location = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    distance_alerts = serializers.BooleanField(required=False)
    alert_radius = serializers.IntegerField(required=False)
