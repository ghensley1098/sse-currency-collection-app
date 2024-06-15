from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("moneycollections/", include("moneyCollections.urls")),
    path("admin/", admin.site.urls),
]