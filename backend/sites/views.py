import re
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, request
from django.core.validators import RegexValidator
from rest_framework.views import APIView
from authentication.views import BaseAuthenticatedView
from companies.services import CompanyService
from companies.views import CompanyDetailView
from sites.services import SiteService
from sites.models import Site
from rest_framework.permissions import IsAuthenticated
from authentication.auth import CustomJWTAuthentication


class SiteDetailView(BaseAuthenticatedView):
    class OutputSerializer(serializers.ModelSerializer):
        company = CompanyDetailView().OutputSerializer()

        class Meta:  # pyright: ignore
            model = Site
            fields = ["id", "name", "postcode", "company", "location"]
            depth = 1

    def get(self, _, id):
        site = SiteService().get(id)

        if site is None:
            raise Http404

        return Response(
            data=self.OutputSerializer(site).data, status=status.HTTP_200_OK
        )


class ListSiteView(APIView):
    def get(self, _):
        sites = SiteService().list()

        return Response(
            data={"sites": SiteDetailView.OutputSerializer(sites, many=True).data},
            status=status.HTTP_200_OK,
        )


def uk_postcode_validator(postcode):
    if re.match(r"^([A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}|GIR ?0A{2})$", postcode) is None:
        raise serializers.ValidationError("Invalid UK postcode.")


class CreateSiteView(BaseAuthenticatedView):
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

        return Response(
            data={
                "site": SiteDetailView.OutputSerializer(site).data,
            },
            status=status.HTTP_201_CREATED,
        )


class UpdateSiteView(BaseAuthenticatedView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        postcode = serializers.CharField(
            required=False, validators=[uk_postcode_validator]
        )

    def patch(self, request, id) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        site = SiteService().get(id)

        if site is None:
            raise Http404

        updated_site = SiteService().update(site, serializer.validated_data)

        return Response(
            data={
                "site": SiteDetailView.OutputSerializer(updated_site).data,
            },
            status=status.HTTP_200_OK,
        )


class DeleteSiteView(BaseAuthenticatedView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, _, id) -> Response:
        site = SiteService().get(id)

        if site is None:
            raise Http404

        SiteService().delete(site)

        return Response(status=status.HTTP_204_NO_CONTENT)
