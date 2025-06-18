import re
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, request
from django.core.validators import RegexValidator
from companies.services import CompanyService
from companies.views import CompanyDetailView
from sites.services import SiteService
from sites.models import Site
from rest_framework.permissions import IsAuthenticated
from authentication.auth import CustomJWTAuthentication


class SiteDetailView(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        company = CompanyDetailView().OutputSerializer()

        class Meta:  # pyright: ignore
            model = Site
            fields = ["id", "name", "postcode", "company"]
            depth = 1

    def get(self, request, user_id):
        site = SiteService().get(user_id)

        if site is None:
            raise Http404

        data = self.OutputSerializer(site).data

        return Response(data)


def uk_postcode_validator(postcode):
    if re.match(r"^([A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}|GIR ?0A{2})$", postcode) is None:
        raise serializers.ValidationError("Invalid UK postcode.")


class CreateSiteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        postcode = serializers.CharField(validators=[uk_postcode_validator])

    def post(self, request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = request.user

        company = CompanyService().get(account.id)
        site = SiteService().create(**serializer.validated_data, company=company)
        print("SITE:", site)

        data = {
            "site": SiteDetailView.OutputSerializer(site).data,
        }

        return Response(data, status.HTTP_201_CREATED)


class UpdateSiteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        postcode = serializers.CharField(
            required=False, validators=[uk_postcode_validator]
        )

    def patch(self, request, id) -> Response:
        print("ARGS:", id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        site = SiteService().get(id)

        if site is None:
            raise Http404

        updated_site = SiteService().update(site, serializer.validated_data)

        data = {
            "site": SiteDetailView.OutputSerializer(updated_site).data,
        }

        return Response(data)


class DeleteSiteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request, id) -> Response:
        print("ID: ", id)
        site = SiteService().get(id)

        if site is None:
            raise Http404

        SiteService().delete(site)

        return Response(status=status.HTTP_204_NO_CONTENT)
