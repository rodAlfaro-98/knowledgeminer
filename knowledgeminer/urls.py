from django.urls import path
from . import views

app_name = "knowledgeminer"

#URLConf
urlpatterns = [
    path('', views.index, name='index'),
    path('ba/', views.ba_prueba, name="ba"),
    path('eda/',views.eda_prueba , name="eda"),
    path('pca/',views.pca_prueba, name="pca"),
    path('ad/',views.ad_prueba, name="ad"),
    path('input/',views.insert_file, name="input"),
    path('register/', views.register_request,name = "register"),
    path('login/', views.login_request, name='login'),
]
