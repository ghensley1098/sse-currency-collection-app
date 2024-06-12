from django.urls import path

from . import views

urlpatterns = [
    path('', views.cryptoApp, name='template'),
]