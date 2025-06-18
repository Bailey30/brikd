from django.urls import path

from sites.views import CreateSiteView, UpdateSiteView, SiteDetailView, DeleteSiteView

app_name = "sites"
urlpatterns = [
    path("create/", CreateSiteView.as_view(), name="create"),
    path("<int:id>", SiteDetailView.as_view(), name="get"),
    path("<int:id>/update", UpdateSiteView.as_view(), name="update"),
    path("<int:id>/delete", DeleteSiteView.as_view(), name="delete"),
]
