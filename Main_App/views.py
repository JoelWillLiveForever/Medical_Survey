import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from matplotlib.style import context
from numpy import block, where
from datetime import datetime

from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.shortcuts import redirect, render
from django.contrib.auth import login, logout

from .PremakedInfo import PremakedInfo
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
        # print(request.POST)
        # post = request.POST.copy()
        # for i in range(0, len(PremakedInfo.UNIVERSITIES)):
        #     print(post['university'])
        #     print(PremakedInfo.UNIVERSITIES[i][1])
        #     if int(post['university']) == i:
        #         print(post['university'])
        #         post.update({'university': post['university'], 'university': PremakedInfo.UNIVERSITIES[i][1]})
        #         break
                    
        # request.POST = post
        # print(request.POST)
        form = RegistrationForm(request.POST)
        #print()
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

            #Изменение полей на основе select-бокса
            post = request.POST.copy()

            #Изменение пола
            for i in range(0, len(PremakedInfo.GENDERS)):
                if int(post['gender']) == i:
                    post.update({'gender': post['gender'], 'gender': PremakedInfo.GENDERS[i][1]})
                    break

            #Изменение названия города из списка названий
            for i in range(0, len(PremakedInfo.CITIES)):
                if int(post['city']) == i:
                    post.update({'city': post['city'], 'city': PremakedInfo.CITIES[i][1]})
                    break

            #Изменение названия учебного заведения из списка названий
            for i in range(0, len(PremakedInfo.UNIVERSITIES)):
                if int(post['university']) == i:
                    post.update({'university': post['university'], 'university': PremakedInfo.UNIVERSITIES[i][1]})
                    break
            #Внесение изменений для созданного выше пользователя
            request.POST = post
            Patient.objects.filter(id=user.id).update(university=request.POST.get('university'), city=request.POST.get('city'), gender=request.POST.get('gender'))

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
    context = {'login_form': LoginForm()}
    if request.method == 'POST' and 'login_button' in request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.login(request)
            if user:
                login(request, user)
                return redirect('profile')

        context = {'login_form': login_form}

    return render(request, 'login_page.html', context)


def profile(request):
    #Контекстная переменная, меняет своё значение в зависимости от добавляемого анализа
    #Влияет на изменение формы для заполнения анализа
    global context_analysis
    #Контекстная переменная, меняет своё значение в зависимости от выбранного блока опроса
    global context_block
    # Вычисление выбранного блока вопросов считыванием с формы через регулярное выражение.
    # Передаём ID выбранного блока на страницу question с помощью обновления глобальной переменной.
    if request.method == 'POST' and re.findall(r'block[0-9]', f'{str(request.POST)}'):
        blockID = re.search(r'block[0-9]', f'{str(request.POST)}').group(0)
        print(re.search(r'[0-9]', blockID).group(0))
        blockID = re.search(r'[0-9]', blockID).group(0)
        print(Question.objects.filter(block__in=re.search(r'[0-9]', blockID).group(0)))
        if Block.objects.filter(id=blockID).exists():
            context_block = blockID
            return redirect('question')

    if request.method == 'POST' and 'add_new_parameters_toMeasure' in request.POST:
        context_analysis = 'Measure'
        return redirect('add_new_analysis')
    if request.method == 'POST' and 'add_new_parameters_toOAK' in request.POST:
        context_analysis = 'OAK'
        return redirect('add_new_analysis')
    if request.method == 'POST' and 'add_new_parameters_toCardio' in request.POST:
        context_analysis = 'Cardio'
        return redirect('add_new_analysis')
    
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

    #Переменные опроса
    survey_blocks = Block.objects.filter()

    # Проверка значений пациентов
    if (patient_height != 0.0 ):
        if (patient_weight != 0.0):
            if (patient_height <= 10.0): # Данные в метрах (вряд-ли конечно есть человек ростом в 10 метров)
                data = {'height': patient_height * 100, 'weight': patient_weight}
                formHW = HeightNWeightForm(data)
            else: # Данные в сантиметрах
                data = {'height': patient_height, 'weight': patient_weight}
                formHW = HeightNWeightForm(data)
        else:
            if (patient_height <= 10.0): # Данные в метрах
                data = {'height': patient_height * 100, 'weight': 0.0}
                formHW = HeightNWeightForm(data)
            else: # Данные в сантиметрах
                data = {'height': patient_height, 'weight': 0.0}
                formHW = HeightNWeightForm(data)
    elif (patient_weight != 0):
        data = {'height': 0.0, 'weight': patient_weight}
        formHW = HeightNWeightForm(data)
    else:
        data = {'height': 0.0, 'weight': 0.0}
        formHW = HeightNWeightForm(data)
    
    parametersOAK=None
    parametersMeasure=None
    parametersCardio=None

    analysis = Analysis.objects.filter(patient=request.user.id)

    if analysis:
        for anal in analysis:
            if anal.type == 'Данные измерений':
                parametersMeasure = Parameter.objects.filter(analysis__in=analysis)
            if anal.type == 'Общий Анализ Крови':
                parametersOAK = Parameter.objects.filter(analysis__in=analysis)
            if anal.type == 'Данные кардиовизора':
                parametersCardio = Parameter.objects.filter(analysis__in=analysis)

    context = {'formHW': formHW, 
               'Universities': PremakedInfo.UNIVERSITIES,
               'ParametersOAK': parametersOAK,
               'ParametersMeasure': parametersMeasure,
               'ParametersCardio': parametersCardio,
               'Survey_Blocks': survey_blocks,
               'Analysis': analysis}

    return render(request, 'profile.html', context)

def add_new_analysis(request):
    analysisForm = None

    if context_analysis == 'Measure':
        analysisForm = MeasurementForm(request.POST)
        print(analysisForm.errors)
    elif context_analysis == 'OAK':
        analysisForm = OAKForm(request.POST)
    elif context_analysis == 'Cardio':
        analysisForm = CardiovisorForm(request.POST)
    elif not context_analysis:
        return redirect('profile')

    if request.method == 'POST' and 'submitAnalysis' in request.POST:
        print(f"Дата анализа: {request.POST['date']}")
        post=request.POST.copy()
        post.update({'date': post['date'], 'date': datetime.strptime(str(post['date']), '%Y-%m-%d').strftime('%d-%m-%Y')})
        request.POST = post
        if analysisForm.is_valid():
            print(f"Дата анализа: {request.POST['date']}")
            analysisForm.save(patient=Patient.objects.get(id=request.user.id))
        return redirect('profile')
    context = {'analysisForm': analysisForm,
               'context_analysis': context_analysis}
    return render(request, 'add_new_analysis.html', context)

def question(request):

    # Выбираем вопросы, принадлежащие блоку через глобальную переменную его ID
    questions = Question.objects.filter(block__in=context_block)
    print(questions)

    context= {
        'Questions': questions,
        'BlockNumber': context_block
    }
    return render(request, 'question.html', context)