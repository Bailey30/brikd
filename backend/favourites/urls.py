from django.urls import path
from favourites.views import (
    CreateFavouriteView,
    DeleteFavouriteView,
    ListFavouritesView,
)

app_name = "favourites"
urlpatterns = [
    path("", ListFavouritesView.as_view(), name="list"),
    path("create", CreateFavouriteView.as_view(), name="create"),
    path("delete", DeleteFavouriteView.as_view(), name="delete"),
]
