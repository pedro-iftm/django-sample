from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html')),
    path('registrar/', views.register),
]