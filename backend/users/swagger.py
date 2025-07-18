from users.serializers import (
    CreateUserInputSerializer,
    UpdateUserInputSerializer,
    UserOutputSerializer,
)


create_user_view_schema = {
    "operation_description": "Creates a user of type 'jobseeker'",
    "request_body": CreateUserInputSerializer,
    "responses": {201: UserOutputSerializer},
}

update_user_view_schema = {
    "operation_description": "Update an existing 'jobseeker' type user.",
    "request_body": UpdateUserInputSerializer,
    "responses": {200: UserOutputSerializer, 404: "Not found."},
}
