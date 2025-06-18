from django.urls import path

from companies.views import CreateSiteApi

app_name = "sites"
urlpatterns = [
    path("create/", CreateSiteApi.as_view(), name="create"),
]
