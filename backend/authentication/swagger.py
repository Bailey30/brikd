from drf_yasg import openapi

get_user_schema = {
    "operation_description": "Get details of the currently authenticated user.",
    "responses": {
        200: openapi.Response(
            description="Returns details of the current user.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(
                        type=openapi.TYPE_INTEGER, description="User ID"
                    ),
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format="email",
                        description="User email address",
                    ),
                    "is_active": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="Whether the user account is active",
                    ),
                    "is_admin": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="Whether the user has admin privileges",
                    ),
                },
                required=["id", "email", "is_active", "is_admin"],
            ),
        ),
        401: openapi.Response(
            description="Authentication credentials were not provided or invalid."
        ),
    },
}
