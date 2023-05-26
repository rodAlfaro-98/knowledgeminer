from django.shortcuts import render
from .scriptsMineria import eda as EDA
from .scriptsMineria import bosque_aleatorio as BA

# Create your views here.
def say_hello(request):
    context = {
        'name': 'Rodrigo',
        'var': 5,
    }
    return render(request=request,template_name='hello.html',context=context)

def eda_prueba(request):
    file_name = 'E:/Windows/FI/carrera/DecimoSemestre/Mineria/practicas/practica1/assets/melb_data.csv'
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
