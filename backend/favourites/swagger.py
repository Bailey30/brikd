from favourites.serializers import FavouriteInputSerializer, FavouriteOutputSerializer


create_favourite_view_schema = {
    "operation_description": "Creates a favourite job object.",
    "request_body": FavouriteInputSerializer,
    "responses": {201: "Favourite created successfully.", 404: "Not found."},
}

list_favourite_view_schema = {
    "operation_description": "Lists all favourites for the logged in user.",
    "responses": {200: FavouriteOutputSerializer},
}

delete_favourite_view_schema = {
    "operation_description": "Delete a favourite job object.",
    "responses": {
        204: "Favourite deleted successfully. No content returned.",
        404: "Not found (either favourite or job).",
    },
}
