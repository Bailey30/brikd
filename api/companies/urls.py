from django.urls import path

from companies.views import CompanyCreateApi, CompanyListApi

app_name = "companies"
urlpatterns = [
    path("", CompanyListApi.as_view(), name=""),
    path("create/", CompanyCreateApi.as_view(), name="create"),
]
