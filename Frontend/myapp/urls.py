from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('help/', views.help),
    path('hello/', views.hello),
    #path('hello/<str:username>', views.hello),
    #en el video me quede en la seccion formularios minuto 2:33:22
]