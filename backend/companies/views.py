from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from common.models import BaseUserSerializer
from companies.models import Company
from companies.services import CompanyService
from django.http import Http404


class CompanyDetailView(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        profile = BaseUserSerializer()

        class Meta:  # pyright: ignore
            model = Company
            fields = ["id", "name", "profile"]
            depth = 1

    def get(self, request, user_id):
        user = CompanyService().get(user_id)

        if user is None:
            raise Http404

        data = self.OutputSerializer(user).data

        return Response(data)


class CompanyListView(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        profile = BaseUserSerializer()

        class Meta:  # pyright: ignore
            model = Company
            fields = ["id", "name", "profile"]
            depth = 1

    def get(self, request) -> Response:
        companys = CompanyService().list()
        serializer = self.OutputSerializer(companys, many=True)
        print("COMPANIES:", serializer.data)
        return Response(serializer.data)


class CompanyCreateView(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
        name = serializers.CharField()

    def post(self, request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = CompanyService().create(**serializer.validated_data)

        data = {
            "user": CompanyDetailView.OutputSerializer(company).data,
        }

        # login(request, company)
        return Response(data, status.HTTP_201_CREATED)
