from drf_yasg import openapi
from sites.serializers import (
    CreateSiteInputSerializer,
    SiteDetailOutputSerializer,
    UpdateSiteInputSerializer,
)


site_detail_view_schema = {
    "operation_description": "Gets a single site.",
    "responses": {200: SiteDetailOutputSerializer, 404: "Not found"},
}

list_site_view_schema = {
    "": {},
    "operation_description": "Gets a list of sites.",
}


create_site_view_schema = {
    "operation_description": "Creates a site. Requires a logged in company account to work.",
    "responses": {201: SiteDetailOutputSerializer},
    "request_body": CreateSiteInputSerializer,
}

update_site_view_schema = {
    "operation_description": "Updates a site.",
    "responses": {200: SiteDetailOutputSerializer, 404: "Not found"},
    "request_body": UpdateSiteInputSerializer,
}

delete_site_view_schema = {
    "operation_description": "Deletes a site with the given ID.",
    "responses": {
        204: openapi.Response(
            description="Site deleted successfully. No content returned."
        ),
        404: openapi.Response(description="Site with this ID does not exist."),
    },
}
