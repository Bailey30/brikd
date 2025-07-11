from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from authentication.views import BaseAuthenticatedView
from companies.services import CompanyService
from sites.serializers import (
    CreateSiteInputSerializer,
    SiteDetailOutputSerializer,
    UpdateSiteInputSerializer,
)
from sites.services import SiteService
from sites.models import Site
from rest_framework.permissions import IsAuthenticated
from authentication.auth import CustomJWTAuthentication
from sites.swagger import (
    site_detail_view_schema,
    list_site_view_schema,
    create_site_view_schema,
    update_site_view_schema,
    delete_site_view_schema,
)


class SiteDetailView(BaseAuthenticatedView):
    @swagger_auto_schema(**site_detail_view_schema)
    def get(self, _, id):
        site = SiteService().get(id)

        try:
            site = SiteService().get(id)
        except Site.DoesNotExist:
            raise NotFound(detail="Site with this ID does not exist.")

        return Response(
            data=SiteDetailOutputSerializer(site).data, status=status.HTTP_200_OK
        )


class ListSiteView(ListAPIView):
    serializer_class = SiteDetailOutputSerializer

    @swagger_auto_schema(**list_site_view_schema)
    def get(self, _):
        sites = SiteService().list()

        return Response(
            data={"sites": SiteDetailOutputSerializer(sites, many=True).data},
            status=status.HTTP_200_OK,
        )


class CreateSiteView(BaseAuthenticatedView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    @swagger_auto_schema(**create_site_view_schema)
    def post(self, request) -> Response:
        serializer = CreateSiteInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = request.user

        company = CompanyService().get(account.id)
        site = SiteService().create(**serializer.validated_data, company=company)

        return Response(
            data={
                "site": SiteDetailOutputSerializer(site).data,
            },
            status=status.HTTP_201_CREATED,
        )


class UpdateSiteView(BaseAuthenticatedView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    @swagger_auto_schema(**update_site_view_schema)
    def patch(self, request, id) -> Response:
        serializer = UpdateSiteInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            site = SiteService().get(id)
        except Site.DoesNotExist:
            raise NotFound(detail="Site with this ID does not exist.")

        updated_site = SiteService().update(site, serializer.validated_data)

        return Response(
            data={
                "site": SiteDetailOutputSerializer(updated_site).data,
            },
            status=status.HTTP_200_OK,
        )


class DeleteSiteView(BaseAuthenticatedView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    @swagger_auto_schema(**delete_site_view_schema)
    def delete(self, _, id) -> Response:
        site = SiteService().get(id)

        try:
            site = SiteService().get(id)
        except Site.DoesNotExist:
            raise NotFound(detail="Site with this ID does not exist.")

        SiteService().delete(site)

        return Response(status=status.HTTP_204_NO_CONTENT)
