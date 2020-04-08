from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


urlpatterns = [
    path('entrar/', auth_views.LoginView.as_view(template_name='login.html')),
    path('entrar/registrar/', views.register),
    path('sair/', auth_views.LogoutView.as_view(template_name='home.html')),
]