from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('solicitarServicio1/', views.servicioUno),
    path('solicitarServicio2/', views.servicioDos),
    path('detalleMensajes/', views.detalleMensajes),
    path('resumenPesos/', views.resumenPesos),
    path('creacionMensaje/', views.creacion1Mensaje),
    path('limpiar/', views.limpiar),
    path('help/', views.help),
    #path('hello/<str:username>', views.hello),
    #en el video me quede en la seccion formularios minuto 2:33:22
]