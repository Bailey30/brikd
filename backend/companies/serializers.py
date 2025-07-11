from rest_framework import serializers
from common.models import BaseUserSerializer
from companies.models import Company


class CompanyDetailOutputSerializer(serializers.ModelSerializer):
    profile = BaseUserSerializer()

    class Meta:  # pyright: ignore
        model = Company
        fields = ["id", "name", "profile"]
        depth = 1


class CompanyListOutputSerializer(serializers.ModelSerializer):
    profile = BaseUserSerializer()

    class Meta:  # pyright: ignore
        model = Company
        fields = ["id", "name", "profile"]
        depth = 1


class CompanyCreateInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    name = serializers.CharField()
