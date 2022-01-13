from django.shortcuts import render

# Create your views here.

def hello(request):

    context= {

    }
    return render(request, 'hello.html', context)

def registration(request):

    context= {

    }
    return render(request, 'registration.html', context)