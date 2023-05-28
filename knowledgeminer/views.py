from django.shortcuts import render, redirect
from .scriptsMineria import eda as EDA
from .scriptsMineria import bosque_aleatorio as BA
from .scriptsMineria import pca as PCAA
from .scriptsMineria import ad as AD
from .forms.UploadFileForm import UploadFileForm
from .forms.Register import NewUserForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import File
import os

def handle_uploaded_file(f,current_user):  
    path = "./knowledgeminer/UserFiles/"+current_user.username
    if not os.path.exists("./knowledgeminer/UserFiles/"+current_user.username):
        directory = current_user.username
        parent_dir = "./knowledgeminer/UserFiles/"
        path = os.path.join(parent_dir,directory)
        os.mkdir(path)
    with open('./knowledgeminer/UserFiles/'+current_user.username+'/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():
            destination.write(chunk)  
    file = File(user=current_user,name = f.name,path = './knowledgeminer/UserFiles/'+current_user.username+'/'+f.name)
    file.save()

# Create your views here.
def insert_file(request):
    if request.user.is_authenticated:
        context = {}
        if request.POST:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES["archivo"],request.user)
        else:
            form = UploadFileForm()
        context['form'] = form
        return render(request, "data_insert.html", context)
    else:
        form = AuthenticationForm()
        return render(request=request, template_name="login.html", context={"login_form":form})

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

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("knowledgeminer:input")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("knowledgeminer:input")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def index(request):
    if request.user.is_authenticated:
        current_user = request.user
        files = File.objects.filter(user = current_user)
        names_files = []
        for file in files:
             names_files.append(file.name)
        context = {
            'files': names_files,
            'username': current_user.username,
        }
        return render(request=request, template_name='index.html',context = context)
    else:
        form = AuthenticationForm()
        return render(request=request, template_name="login.html", context={"login_form":form})