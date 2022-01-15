from django.shortcuts import render
from django.shortcuts import redirect, render

# Create your views here.

def hello(request):

    if request.method == 'POST' and 'toSurveyBtn' in request.POST:
        return redirect('registration')
    context= {

    }
    return render(request, 'hello.html', context)

def registration(request):

    context= {

    }
    return render(request, 'registration.html', context)