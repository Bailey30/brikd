from companies.serializers import (
    CompanyCreateInputSerializer,
    CompanyDetailOutputSerializer,
    CompanyListOutputSerializer,
)

company_detail_view_schema = {
    "operation_description": "Gets one company.",
    "responses": {200: CompanyListOutputSerializer, 404: "Not found."},
}

list_company_view_schema = {
    "operation_description": "Gets a list of companies.",
    "responses": {200: CompanyDetailOutputSerializer},
}

create_company_view_schema = {
    "operation_description": "Creates a company.",
    "request_body": CompanyCreateInputSerializer,
    "responses": {201: CompanyDetailOutputSerializer},
}
