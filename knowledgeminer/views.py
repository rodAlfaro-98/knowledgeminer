from django.shortcuts import render
from .scriptsMineria import eda as EDA
from .scriptsMineria import bosque_aleatorio as BA
from .scriptsMineria import pca as PCAA
from .scriptsMineria import ad as AD

# Create your views here.
def say_hello(request):
    context = {
        'name': 'Rodrigo',
        'var': 5,
    }
    return render(request=request,template_name='hello.html',context=context)

def eda_prueba(request):
    file_name = 'E:/Windows/FI/carrera/DecimoSemestre/Mineria/practicas\practica1/assets/country_vaccinations.csv'
    eda = EDA.initialization(file_name)
    context = {
        'eda': eda,
        'file': file_name,
    }
    return render(request = request, template_name='eda.html', context = context)

def ba_prueba(request):
    file_name = 'E:/Windows/FI/carrera/DecimoSemestre/Mineria/practicas/practica13/Datos/diabetes.csv'
    ba = BA.initialization(file_name,'Outcome')
    context = {
        'ba': ba,
        'file': file_name,
    }
    return render(request = request, template_name='ba.html', context = context)
def pca_prueba(request):
    file_name = 'E:/Windows/FI/carrera/DecimoSemestre/Mineria/practicas/practica4/assets/Hipoteca.csv'
    pca = PCAA.initialization(file_name)
    context = {
        'pca': pca,
        'file': file_name,
    }
    return render(request = request, template_name = 'pca.html', context = context)

def ad_prueba(request):
    file_name = 'E:/Windows/FI/carrera/DecimoSemestre/Mineria/practicas/practica13/Datos/diabetes.csv'
    ad = AD.initialization(file_name)
    context = {
        'ad': ad,
        'file': file_name,
    }
    return render(request = request, template_name = 'ad.html', context = context)
