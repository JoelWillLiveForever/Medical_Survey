from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.shortcuts import redirect, render
from django.contrib.auth import login, logout

from .models import *
from .forms import *

# Create your views here.

def hello(request):

    if request.method == 'POST' and 'toSurveyBtn' in request.POST:
        return redirect('registration')
    if request.method == 'POST' and 'toProfileBtn' in request.POST:
        return redirect('login_page')
    context= {

    }
    return render(request, 'hello.html', context)

def registration(request):
    # if request.user.is_authenticated:
    #     pass
    #     # return redirect('.html')
    if request.method == 'POST' and 'next_button':    
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            # Sending activation link in terminal
            mail_subject = 'Медицинский опрос. Активация аккаунта.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('acc_active_sent')
        context= {
            'regForm': form,
        }
        return render(request, 'registration.html', context)
    elif request.method == 'POST' and 'back_button' in request.POST:
        return redirect('hello')
    form = RegistrationForm()
    context= {
        'regForm': form,
    }
    return render(request, 'registration.html', context)

# активация акков
def acc_active_sent(request):
    return render(request, 'acc_active_sent.html')

def acc_active_confirmed(request):
    if request.method == 'POST' and 'back_button' in request.POST:
        return redirect('login_page')
    return render(request, 'acc_active_confirmed.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    print(user)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('acc_active_confirmed')
    else:
        return HttpResponse('Activation link is invalid!')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile')

    # error = ''
    # if request.method == 'POST' and request.method == 'GET' and 'back_button' in request.GET:
    #     return redirect('home')
    if request.method == 'POST' and 'login_button' in request.POST:
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')

            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('profile')

    form = LoginForm()
    context = {'login_form': form}

    return render(request, 'login_page.html', context)

def profile(request):
    if request.method == 'POST' and 'button_logout' in request.POST:
        logout(request)
        return redirect('login_page')
    if request.method == 'POST' and ('height' or 'weight') in request.POST:
        form = HeightNWeightForm(request.POST)
        if form.is_valid(): # Изменение значений роста и веса
            Patient.objects.filter(id=request.user.id).update(height=request.POST.get('height'), weight=request.POST.get('weight'))
    
    # Создание пациентов для вывода их текущих значений
    patient_height = Patient.objects.filter(id=request.user.id).get().height
    patient_weight = Patient.objects.filter(id=request.user.id).get().weight
    # print(patient_height)
    # print(patient_weight)

    # Проверка значений пациентов
    if (patient_height != 0.0 ):
        if (patient_weight != 0.0):
            data = {'height': patient_height, 'weight': patient_weight}
            formHW = HeightNWeightForm(data)
        else:
            data = {'height': patient_height, 'weight': 0.0}
            formHW = HeightNWeightForm(data)
    elif (patient_weight != 0):
        data = {'height': 0.0, 'weight': patient_weight}
        formHW = HeightNWeightForm(data)
    else:
        data = {'height': 0.0, 'weight': 0.0}
        formHW = HeightNWeightForm(data)

    #formHW = HeightNWeightForm()
    context = {'formHW': formHW}

    return render(request, 'profile.html', context)

def questionA(request):
    context= {
        
    }
    return render(request, 'questionA.html', context)