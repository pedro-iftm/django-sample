from django.urls import path, re_path, include
from . import views


app_name = 'courses'
urlpatterns = [
    path('', views.courses),
    path('<slug:slug>/', views.details),
    path('<slug:slug>/inscricao', views.enrollment),
    path('<slug:slug>/cancelar', views.undo_enrollment),
    path('<slug:slug>/aulas', views.lessons),
    path('<slug:slug>/aula/<str:pk>', views.lesson),
    path('<slug:slug>/aula/<str:lesson_pk>/material/<str:pk>', views.material),
]