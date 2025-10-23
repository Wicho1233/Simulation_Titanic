from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ejemplo-sobrevive/', views.ejemplo_sobrevive, name='ejemplo_sobrevive'),
    path('ejemplo-no-sobrevive/', views.ejemplo_no_sobrevive, name='ejemplo_no_sobrevive'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
]