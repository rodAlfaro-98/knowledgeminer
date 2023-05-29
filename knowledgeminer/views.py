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

def create_user_dir(username):
    directory = username
    parent_dir = "./knowledgeminer/UserFiles/"
    path = os.path.join(parent_dir,directory)
    os.mkdir(path)

def handle_uploaded_file(f,current_user):  
    path = "./knowledgeminer/UserFiles/"+current_user.username+"/"
    with open(path+f.name, 'wb+') as destination:  
        for chunk in f.chunks():
            destination.write(chunk)  
    file = File(user=current_user,name = f.name,path =path+f.name)
    file.save()

# Create your views here.
def insert_file(request):
    if request.user.is_authenticated:
        context = {}
        if request.POST:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES["archivo"],request.user)
                return redirect("knowledgeminer:index")
        else:
            form = UploadFileForm()
        context['form'] = form
        return render(request=request, context=context, template_name='data_insert.html')
    else:
        form = AuthenticationForm()
        return render(request=request, template_name="login.html", context={"login_form":form})

def eda_prueba(request):
    file_name = request.session['archivo']
    file = file_name.split('/')[len(file_name.split('/'))-1]
    eda = EDA.initialization(file_name)
    context = {
        'eda': eda,
        'file': file,
    }
    return render(request = request, template_name='eda.html', context = context)

def ba_prueba(request):
    file_name = request.session['archivo']
    ba = BA.initialization(file_name,'Outcome')
    file = file_name.split('/')[len(file_name.split('/'))-1]
    context = {
        'ba': ba,
        'file': file,
    }
    return render(request = request, template_name='ba.html', context = context)
def pca_prueba(request):
    file_name = request.session['archivo']
    file = file_name.split('/')[len(file_name.split('/'))-1]
    pca = PCAA.initialization(file_name)
    context = {
        'pca': pca,
        'file': file,
    }
    return render(request = request, template_name = 'pca.html', context = context)

def ad_prueba(request):
    file_name = request.session['archivo']
    file = file_name.split('/')[len(file_name.split('/'))-1]
    ad = AD.initialization(file_name)
    context = {
        'ad': ad,
        'file': file,
    }
    return render(request = request, template_name = 'ad.html', context = context)

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            create_user_dir(user.username)
            messages.success(request, "Registration successful." )
            return redirect("knowledgeminer:index")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
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
				return redirect("knowledgeminer:index")
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
    
def seleccion(request):
    archivo = ''
    current_user = request.user
    if request.POST['archivos'] != 'default':
        archivo = "./knowledgeminer/UserFiles/"+current_user.username+"/"+request.POST['archivos']
    else:
        archivo = "./knowledgeminer/UserFiles/default"+request.POST['archivos_default']
    request.session['archivo'] = archivo
    algoritmo = request.POST['algoritmo']
    if algoritmo == 'eda' :
        return redirect("knowledgeminer:eda")
    elif algoritmo == 'pca':
        return redirect("knowledgeminer:pca")
    elif algoritmo == 'ad':
        return redirect("knowledgeminer:ad")
    elif algoritmo == 'ba':
        return redirect("knowledgeminer:ba")
    else:
        messages.error(request,"Favor de elegir un archivo y algoritmo")
        return redirect("knowledgeminer:index")