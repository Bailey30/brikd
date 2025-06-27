from django.urls import path

from companies.views import CompanyCreateView, CompanyListView

app_name = "companies"
urlpatterns = [
    path("", CompanyListView.as_view(), name=""),
    path("create/", CompanyCreateView.as_view(), name="create"),
]
