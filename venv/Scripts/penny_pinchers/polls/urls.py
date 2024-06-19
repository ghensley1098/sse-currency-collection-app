from django.urls import path
#from .views import SignUpView

from . import views

app_name = "mcollections"
urlpatterns = [
    path('signup/', views.custom_signup_view, name='signup'),
    path('login/', views.custom_login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/<collection>', views.dashboard_view, name='dashboard_specific'),
    path('dashboard/<collection>/new', views.newEntryView, name='new_entry'),
    path('entry/<name>', views.modifyEntryView, name='entry_specific')
]