from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from companies.services import CompanyService
from companies.views import companyDetailApi
from sites.services import SiteService
from sites.models import Site
from rest_framework.permissions import IsAuthenticated
from authentication.auth import CustomJWTAuthentication


class SiteDetailApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:  # pyright: ignore
            model = Site
            fields = ["id", "name", "postcode"]

    def get(self, request, user_id):
        user = SiteService().get(user_id)

        if user is None:
            raise Http404

        data = self.OutputSerializer(user).data

        return Response(data)


class CreateSiteApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        postcode = serializers.CharField()

    def post(self, request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = request.user
        company = CompanyService().get(account.id)
        site = SiteService().create(**serializer.validated_data, company=company)

        data = {
            "user": SiteDetailApi.OutputSerializer(site).data,
        }

        return Response(data, status.HTTP_201_CREATED)


# Create your views here.
