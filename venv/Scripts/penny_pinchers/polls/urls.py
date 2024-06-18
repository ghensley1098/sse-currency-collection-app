from django.urls import path
#from .views import SignUpView

from . import views

app_name = "mcollections"
urlpatterns = [
    path('signup/', views.custom_signup_view, name='signup'),
    path('login/', views.custom_login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]