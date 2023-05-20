from django.shortcuts import render

# Create your views here.
def say_hello(request):
    context = {
        'name': 'Rodrigo',
        'var': 5,
    }
    return render(request=request,template_name='hello.html',context=context)