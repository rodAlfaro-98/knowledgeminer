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
    path('seleccion/', views.seleccion, name='seleccion'),
    path('exportar/',views.exportar, name = 'exportar'),
    path('export/pca/<str:columnas>/<str:porcentaje>',views.exportar_pca, name = 'exportar_pca'),
    path('export_pdf/',views.exportar_pdf,name='exportar_pdf'),
    path('export_pdf/exportacion/',views.seleccion_pdf,name='seleccion_pdf'),
    path('logount/',views.logout_view, name='logout'),
    path('comparacion/', views.comparacion, name='cab'),
]
