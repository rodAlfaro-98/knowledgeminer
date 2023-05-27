from django.shortcuts import render
from .scriptsMineria import eda as EDA
from .scriptsMineria import bosque_aleatorio as BA
from .scriptsMineria import pca as PCAA
from .scriptsMineria import ad as AD
from .forms.UploadFileForm import UploadFileForm

def handle_uploaded_file(f):  
    with open('./knowledgeminer/UserFiles/default/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():
            destination.write(chunk)  
# Create your views here.
def insert_file(request):
    context = {}
    if request.POST:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["archivo"])
    else:
        form = UploadFileForm()
    context['form'] = form
    return render(request, "data_insert.html", context)

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

