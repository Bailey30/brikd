from django.urls import path
from users.views import CreateUserView, UpdateUserView

app_name = "users"
urlpatterns = [
    path("create", CreateUserView.as_view(), name="create"),
    path("<int:id>/update", UpdateUserView.as_view(), name="update"),
]
