from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    path('eda/', views.eda_prueba),
    path('ba/', views.ba_prueba)
]