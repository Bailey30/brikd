from drf_yasg import openapi
from jobs.serializers import (
    JobOutputSerializer,
    CreateJobInputSerializer,
    UpdateJobInputSerializer,
)

job_detail_view_schema = {
    "operation_description": "Gets a single job.",
    "responses": {200: JobOutputSerializer, 404: "Not found"},
}

list_job_view_schema = {
    "operation_description": "Gets a list of jobs.",
    "manual_parameters": [
        openapi.Parameter(
            "postcode",
            openapi.IN_QUERY,
            description="Postcode used to compare distance.",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "distance",
            openapi.IN_QUERY,
            description="Used to filter jobs within this distance to the provided postcode.",
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            "sort",
            openapi.IN_QUERY,
            description="How the jobs should be sorted.",
            type=openapi.TYPE_STRING,
            enum=[
                "newest",
                "oldest",
                "distance_closest",
                "distance_furthest",
                "hourly_rate_highest",
                "hourly_rate_lowest",
            ],
        ),
    ],
}

create_job_view_schema = {
    "operation_description": "Creates a job.",
    "responses": {201: JobOutputSerializer},
    "request_body": CreateJobInputSerializer,
}

update_job_view_schema = {
    "request_body": UpdateJobInputSerializer,
    "responses": {200: JobOutputSerializer, 404: "Not found"},
}

delete_job_view_schema = {
    "operation_description": "Deletes a job with the given ID.",
    "responses": {
        204: openapi.Response(
            description="Job deleted successfully. No content returned."
        ),
        404: openapi.Response(description="Job with this ID does not exist."),
    },
}
