from django.http import Http404
from rest_framework.exceptions import ValidationError
from common.pagination import LimitOffsetPagination, get_paginated_response
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.views import BaseAuthenticatedView
from companies.views import CompanyDetailView
from jobs.models import Job
from jobs.services import JobService
from sites.views import SiteDetailView


class JobOutputSerializer(serializers.ModelSerializer):
    company = CompanyDetailView().OutputSerializer()
    site = SiteDetailView().OutputSerializer()

    class Meta:  # pyright: ignore
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "hourly_rate",
            "daily_rate",
            "company",
            "site",
        ]


class JobDetailView(APIView):
    def get(self, _, id) -> Response:
        job = JobService().get(id)

        if job is None:
            raise Http404

        return Response(
            data={"job": JobOutputSerializer(job).data}, status=status.HTTP_200_OK
        )


class ListJobView(APIView):
    class Pagination(LimitOffsetPagination):
        pass

    class JobOutputSerializer(serializers.ModelSerializer):
        company = CompanyDetailView().OutputSerializer()
        site = SiteDetailView().OutputSerializer()
        distance = serializers.CharField(required=False)

        class Meta:  # pyright: ignore
            model = Job
            fields = [
                "id",
                "title",
                "description",
                "hourly_rate",
                "daily_rate",
                "company",
                "site",
                "distance",
            ]

    def get(self, request) -> Response:
        params = request.GET

        jobs = JobService().filter(params)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.JobOutputSerializer,
            queryset=jobs,
            request=request,
            view=self,
        )


class CreateJobView(BaseAuthenticatedView):
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        hourly_rate = serializers.IntegerField(required=False)
        daily_rate = serializers.IntegerField(required=False)
        company_id = serializers.CharField()
        site_id = serializers.CharField()

    def post(self, request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = JobService().create(**serializer.validated_data)

        return Response(
            data={"job": JobOutputSerializer(job).data}, status=status.HTTP_201_CREATED
        )


class UpdateJobView(BaseAuthenticatedView):
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)
        description = serializers.CharField(required=False)
        hourly_rate = serializers.IntegerField(required=False)
        daily_rate = serializers.IntegerField(required=False)
        company_id = serializers.CharField(required=False)
        site_id = serializers.CharField(required=False)

    def patch(self, request, id) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = JobService().get(id)

        updated_job = JobService().update(job, serializer.validated_data)

        return Response(
            data={"job": JobOutputSerializer(updated_job).data},
            status=status.HTTP_200_OK,
        )


class DeleteJobView(BaseAuthenticatedView):
    def post(self, _, id) -> Response:
        job = JobService().get(id)

        if job is None:
            raise Http404

        JobService().delete(job)

        return Response(status=status.HTTP_204_NO_CONTENT)
