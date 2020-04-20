from django.urls import path, re_path, include
from . import views


app_name = 'courses'
urlpatterns = [
    path('', views.courses),
    path('<slug:slug>/', views.details),
    path('<slug:slug>/inscricao', views.enrollment)
]