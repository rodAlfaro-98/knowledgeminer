from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    path('ba/', views.ba_prueba),
    path('eda/',views.eda_prueba),
    path('pca/',views.pca_prueba),
    path('ad/',views.ad_prueba),
]
