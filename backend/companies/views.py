from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from common.models import BaseUserSerializer
from companies.models import Company
from companies.serializers import (
    CompanyCreateInputSerializer,
    CompanyDetailOutputSerializer,
    CompanyListOutputSerializer,
)
from companies.services import CompanyService
from django.http import Http404
from companies.swagger import (
    company_detail_view_schema,
    list_company_view_schema,
    create_company_view_schema,
)


class CompanyDetailView(APIView):
    @swagger_auto_schema(**company_detail_view_schema)
    def get(self, _, user_id):
        try:
            user = CompanyService().get(user_id)
        except Company.DoesNotExist:
            return NotFound("Company with this ID does not exist.")

        if user is None:
            raise Http404

        return Response(data=CompanyDetailOutputSerializer(user).data)


class CompanyListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(**list_company_view_schema)
    def get(self, _) -> Response:
        companies = CompanyService().list()
        serializer = CompanyListOutputSerializer(companies, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CompanyCreateView(APIView):
    @swagger_auto_schema(**create_company_view_schema)
    def post(self, request) -> Response:
        serializer = CompanyCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = CompanyService().create(**serializer.validated_data)

        return Response(
            data={
                "company": CompanyDetailOutputSerializer(company).data,
            },
            status=status.HTTP_201_CREATED,
        )
