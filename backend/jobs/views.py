from django.http import Http404
from rest_framework.exceptions import NotFound, ValidationError
from common.pagination import LimitOffsetPagination, get_paginated_response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.views import BaseAuthenticatedView
from jobs.models import Job
from jobs.services import JobService
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from jobs.swagger import (
    list_job_view_schema,
    job_detail_view_schema,
    create_job_view_schema,
    update_job_view_schema,
    delete_job_view_schema,
)
from jobs.serializers import (
    JobListOutputSerializer,
    JobOutputSerializer,
    CreateJobInputSerializer,
    UpdateJobInputSerializer,
)


class JobDetailView(APIView):
    @swagger_auto_schema(**job_detail_view_schema)
    def get(self, _, id) -> Response:
        try:
            job = JobService().get(id)
        except Job.DoesNotExist:
            raise NotFound(detail="Job with this ID does not exist.")

        return Response(
            data={"job": JobOutputSerializer(job).data}, status=status.HTTP_200_OK
        )


class ListJobView(ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = JobListOutputSerializer

    @swagger_auto_schema(**list_job_view_schema)
    def get(self, request) -> Response:
        params = request.GET

        # TODO: get jobs for one company or one site.

        try:
            jobs = JobService().list(params)
        except ValidationError as e:
            raise e

        return get_paginated_response(
            pagination_class=self.pagination_class,
            serializer_class=self.serializer_class,
            queryset=jobs,
            request=request,
            view=self,
        )


class CreateJobView(BaseAuthenticatedView):
    @swagger_auto_schema(**create_job_view_schema)
    def post(self, request) -> Response:
        serializer = CreateJobInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = JobService().create(**serializer.validated_data)

        return Response(
            data={"job": JobOutputSerializer(job).data}, status=status.HTTP_201_CREATED
        )


class UpdateJobView(BaseAuthenticatedView):
    @swagger_auto_schema(**update_job_view_schema)
    def patch(self, request, id) -> Response:
        serializer = UpdateJobInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            job = JobService().get(id)
        except Job.DoesNotExist:
            raise NotFound(detail="Job with this ID does not exist.")

        updated_job = JobService().update(job, serializer.validated_data)

        return Response(
            data={"job": JobOutputSerializer(updated_job).data},
            status=status.HTTP_200_OK,
        )


class DeleteJobView(BaseAuthenticatedView):
    @swagger_auto_schema(**delete_job_view_schema)
    def delete(self, _, id) -> Response:
        try:
            job = JobService().get(id)
        except Job.DoesNotExist:
            raise NotFound(detail="Job with this ID does not exist.")

        JobService().delete(job)

        return Response(status=status.HTTP_204_NO_CONTENT)
