from django.shortcuts import render
from .scriptsMineria import eda as EDA
from .scriptsMineria import pca as PCA

# Create your views here.
def say_hello(request):
    context = {
        'name': 'Rodrigo',
        'var': 5,
    }
    return render(request=request,template_name='hello.html',context=context)

def eda_prueba(request):
    file_name = 'E:/Windows/FI/carrera/DecimoSemestre/Mineria/practicas/practica1/assets/country_vaccinations.csv'
    eda = EDA.initialization(file_name)
    context = {
        'eda': eda,
        'file': file_name,
    }
    return render(request = request, template_name='eda.html', context = context)

def pca_prueba(request):
    file_name = 'C:/Users/offue/Downloads/Hipoteca.csv'
    pca = PCA.initialization(file_name)
    context = {
        'pca': pca,
        'file': file_name,
    }
    return render(request = request, template_name = 'pca.html', context = context)
