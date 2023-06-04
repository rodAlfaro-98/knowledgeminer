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
import pandas as pd
from .utils import render_to_pdf
from django.http import HttpResponse
import datetime

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
    df = pd.read_csv(path+f.name)
    file = File(user=current_user,name = f.name,path =path+f.name, columns = list(df.columns) )
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
    ba = BA.initialization(file_name,request.session['var_dep'])
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
    ad = AD.initialization(file_name,request.session['var_dep'])
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
            return render (request=request, template_name="register.html", context={"register_form":form})

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
            'names': names_files,
            'files': files,
            'username': current_user.username,
        }
        return render(request=request, template_name='index.html',context = context)
    else:
        form = AuthenticationForm()
        return render(request=request, template_name="login.html", context={"login_form":form})
    
def seleccion(request):
    archivo = ''
    current_user = request.user
    path = ''
    nombre_archivo = ''
    if 'archivos' in request.POST:
        if request.POST['archivos'] != 'default':
            archivo = "./knowledgeminer/UserFiles/"+current_user.username+"/"+request.POST['archivos']
            path = "./knowledgeminer/UserFiles/"+current_user.username+"/"
            nombre_archivo = request.POST['archivos']
        else:
            archivo = "./knowledgeminer/UserFiles/default/"+request.POST['archivos_default']
            path = "./knowledgeminer/UserFiles/default/"
            nombre_archivo = request.POST['archivos_default']
    else:
        archivo = "./knowledgeminer/UserFiles/default/"+request.POST['usuario_default']
        path = "./knowledgeminer/UserFiles/default/"
        nombre_archivo = request.POST['usuario_default']
    request.session['archivo'] = archivo
    request.session['path'] = path
    request.session['nombre_archivo'] = nombre_archivo
    if 'var_dep' in request.session:
        del request.session['var_dep']
    algoritmo = request.POST['algoritmo']
    if algoritmo == 'eda' :
        return redirect("knowledgeminer:eda")
    elif algoritmo == 'pca':
        return redirect("knowledgeminer:pca")
    elif algoritmo == 'ad':
        if request.POST['archivos'] != 'default':
            var_dep = request.POST[request.POST['archivos']]
            request.session['var_dep'] = var_dep
        return redirect("knowledgeminer:ad")
    elif algoritmo == 'ba':
        if request.POST['archivos'] != 'default':
            var_dep = request.POST[request.POST['archivos']]
            request.session['var_dep'] = var_dep
        return redirect("knowledgeminer:ba")
    else:
        messages.error(request,"Favor de elegir un archivo y algoritmo")
        return redirect("knowledgeminer:index")
    
def exportar(request):
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
    
def exportar_pca(request,columnas,porcentaje):
    columns = [i[16:] for i in columnas.replace('\"','').split(',')]
    columns = [i[:-16] if i[len(i)-1] == ' ' else i for i in columns]
    context = {
        'var':columns
    }
    file_name = request.session['nombre_archivo']
    file_names = file_name.split('.')
    file_name = file_names[0]+'_pca_'+str(len(columns))+'_vars_'+str(porcentaje)+'%.'+file_names[1]
    current_user  = request.user
    request.session['archivo'], request.session['path'], request.session['nombre_archivo'] = newFile(file_name,request.session['archivo'],columns,current_user,request.session['path'])
    messages.success(request, "Se creó el nuevo archivo con los datos seleccionados en el proceso de pca" )
    return redirect("knowledgeminer:index")

def newFile(file_name,original_file,columns,current_user,path):
    df = pd.read_csv(original_file)
    df2 = df.select_dtypes(include=['object'])
    df3 = df[columns]
    df_final = pd.concat([df3,df2], axis = 1, join='inner')
    df_final.to_csv(path+file_name,index = False)
    if File.objects.filter(path=path+file_name).count() == 0:
        file = File(user=current_user,name = file_name,path =path+file_name, columns = list(df_final.columns) )
        file.save()
    return [path+file_name,path,file_name]

def exportar_pdf(request):
    if request.user.is_authenticated:
        current_user = request.user
        files = File.objects.filter(user = current_user)
        names_files = []
        for file in files:
            names_files.append(file.name)
        context = {
            'names': names_files,
            'files': files,
            'username': current_user.username,
        }
        return render(request=request, template_name='choose_export.html',context = context)
    else:
        form = AuthenticationForm()
        return render(request=request, template_name="login.html", context={"login_form":form})
    
def seleccion_pdf(request):
    archivo = ''
    current_user = request.user
    path = ''
    nombre_archivo = ''
    template = 'to_export/'
    if 'archivos' in request.POST:
        if request.POST['archivos'] != 'default':
            archivo = "./knowledgeminer/UserFiles/"+current_user.username+"/"+request.POST['archivos']
            path = "./knowledgeminer/UserFiles/"+current_user.username+"/"
            nombre_archivo = request.POST['archivos']
        else:
            archivo = "./knowledgeminer/UserFiles/default/"+request.POST['archivos_default']
            path = "./knowledgeminer/UserFiles/default/"
            nombre_archivo = request.POST['archivos_default']
    else:
        archivo = "./knowledgeminer/UserFiles/default/"+request.POST['usuario_default']
        path = "./knowledgeminer/UserFiles/default/"
        nombre_archivo = request.POST['usuario_default']
    
    file = archivo
    data = {
        'file': file
    }
    algoritmo = request.POST['algoritmo']
    if algoritmo == 'eda' :
        template +='eda.html'
        eda = EDA.initialization(file)
        data['eda'] = eda
    elif algoritmo == 'pca':
        template +='pca.html'
        pca = PCAA.initialization(file)
        data['pca'] = pca
    elif algoritmo == 'ad':
        template +='ad.html'
        if request.POST['archivos'] != 'default':
            var_dep = request.POST[request.POST['archivos']]
            ad = AD.initialization(file,var_dep)
            data['ad'] = ad
    elif algoritmo == 'ba':
        template +='ba.html'
        if request.POST['archivos'] != 'default':
            var_dep = request.POST[request.POST['archivos']]
            ba = BA.initialization(file,var_dep)
            data['ba'] = ba
    else:
        messages.error(request,"Favor de elegir un archivo y algoritmo")
        return redirect("knowledgeminer:index")
    
    pdf = render_to_pdf(template_src= template,context_dict= data, fileName=algoritmo+"_"+nombre_archivo+".pdf")
    return pdf
    """if pdf:
        print("rendered pdf")
        response = HttpResponse(pdf, content_type="application/pdf")
        filename = algoritmo+"_"+nombre_archivo+"_%s.pdf" %('12341231')
        download = request.GET.get("download")
        if download:
            print("Downloadable")
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response"""
    return HttpResponse("Not found!")