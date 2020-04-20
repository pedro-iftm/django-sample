from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.dashboard),
    path('entrar/', auth_views.LoginView.as_view(template_name='login.html')),
    path('sair/', auth_views.LogoutView.as_view(template_name='home.html')),
    path('registrar/', views.register),
    path('editar/', views.edit),
    path('editar/senha', views.edit_password),
]