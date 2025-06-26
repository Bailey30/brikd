from django.urls import path

from jobs.views import (
    ListJobView,
    CreateJobView,
    UpdateJobView,
    DeleteJobView,
    JobDetailView,
    JobFilterView,
)


app_name = "jobs"
urlpatterns = [
    path("", ListJobView.as_view(), name="list"),
    path("filter/", JobFilterView.as_view(), name="filter"),
    path("create/", CreateJobView.as_view(), name="create"),
    path("<int:id>", JobDetailView.as_view(), name="get"),
    path("<int:id>/update", UpdateJobView.as_view(), name="update"),
    path("<int:id>/delete", DeleteJobView.as_view(), name="delete"),
]
