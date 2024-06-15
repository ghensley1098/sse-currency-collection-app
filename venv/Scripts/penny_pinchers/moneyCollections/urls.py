from django.urls import path

from . import views

app_name = "mcollections"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:collection_id>/", views.detail, name='detail'),
]