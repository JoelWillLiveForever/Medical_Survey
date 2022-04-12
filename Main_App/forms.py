from email.policy import default
from pyexpat import model
from unicodedata import name
from urllib import request
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date, timedelta
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from typing import Iterable
import time
from datetime import datetime
from .PremakedInfo import PremakedInfo
from matplotlib import widgets

# from abc import ABC, abstractmethod

# from django.core.validators import validate_email
# from django.contrib.auth.password_validation import validate_password

from .models import *

MONTHS = {
    1:('Январь'), 2:('Февраль'), 3:('Март'), 4:('Апрель'),
    5:('Май'), 6:('Июнь'), 7:('Июль'), 8:('Август'),
    9:('Сентябрь'), 10:('Октябрь'), 11:('Ноябрь'), 12:('Декабрь')
    }

YEARS = []
for i in range(0, 2021-1920): #Заполнение селектора дат годами от 1922 до 2022
    YEARS.append(str((i-2022)*-1))

class PatientCreationForm(UserCreationForm):

    class Meta:
        model = Patient
        fields = ('email', 'phone', 'surname', 'name', 'lastname', 'city', 'university', 'faculty', 'gender', 'birth_date', 'height', 'weight', 'age', 'password')


class PatientChangeForm(UserChangeForm):

    class Meta:
        model = Patient
        fields = ('email', 'phone', 'surname', 'name', 'lastname', 'city', 'university', 'faculty', 'gender', 'birth_date', 'height', 'weight', 'age', 'password')

class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label='Email', max_length=320)
    password = forms.CharField(required=True, label='Пароль', max_length=320, widget=forms.PasswordInput)

    error_messages = {
        'not_user': 'Неправильный Email или пароль!',
        'error': 'Форма не валидна!',
    }

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password',
       )
       
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError(
                self.error_messages['not_user'],
                code='not_user',
            )
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user

class HeightNWeightForm(UserChangeForm):
    # Форма для изменения параметров роста и веса пациента
    height = forms.FloatField(required=False, label='Рост:', initial=0.0)
    weight = forms.FloatField(required=False, label='Вес:', initial=0.0)

    class Meta: 
        model = Patient # для начала добавить поля в модель пациента
        fields = (
            'height',
            'weight',
       )

class RegistrationForm(UserCreationForm):

    surname = forms.CharField(required=True, label='* Фамилия', max_length=320, help_text='Не более 320 символов')
    name = forms.CharField(required=True, label='* Имя', max_length=320, help_text='Не более 320 символов')
    lastname = forms.CharField(required=False, label='* Отчество', max_length=320, help_text='Не более 320 символов')

    city = forms.ChoiceField(required=True, label='* Регион прописки', choices=PremakedInfo.CITIES)
    university = forms.ChoiceField(required=True, label='* Университет', choices=PremakedInfo.UNIVERSITIES)
    faculty = forms.CharField(required=False, label='* Факультет', max_length=320, help_text='Используя сокращение прим. "ФИТКБ"')

    gender = forms.ChoiceField(required=True, label='* Пол', choices=PremakedInfo.GENDERS)

    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=YEARS, months=MONTHS), label='* Дата рождения')

    email = forms.EmailField(required=True, label='* Адрес электронной почты', max_length=320, help_text='Не более 320 символов')

    phone = forms.CharField(required=True, label='* Номер телефона', max_length=18, help_text="Формат '+7' или '8'")

    password1 = forms.CharField(required=True, label='* Пароль', max_length=320, widget=forms.PasswordInput, help_text='Не менее 8 символов, цифры и верхний регистр')
    password2 = forms.CharField(required=True, label='* Повторите пароль', max_length=320, widget=forms.PasswordInput, help_text='Не менее 8 символов, цифры и верхний регистр')
    agreement = forms.BooleanField(required=True, widget=forms.CheckboxInput)

    error_messages = {
        'email_exists': 'Пользователь с таким Email уже существует!',
        'phone_exists': 'Пользователь с указанным номером телефона уже существует!',
        'choise_city': 'Выберите регион прописки из списка!',
        'choise_university': 'Выберите учебное заведение из списка!',
        'choise_gender': 'Укажите ваш пол!',
        'password_mismatch': 'Пароли не совпадают!',
        'birthdate_isNotYet': 'Дата рождения указывает на то, что вы ещё не родились! Укажите прошедшую дату, если вы не из будущего.',
        'notAgreed': 'Согласитесь на обработку персональных данных или валите!',
        'error': 'Форма не валидна!',
    }

    class Meta:
        model = get_user_model()
        help = {
           'surname': 'Не более 320 символов',
           'surname': 'ПЕТУХ',
        }
        fields = (
            'surname',
            'name',
            'lastname',
            'city',
            'university',
            'faculty',
            'gender',
            'birth_date',
            'email',
            'phone',
            'password1',
            'password2',
       )

    def clean_password(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return self.data['password1']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
            )
        return email
    def clean_birth_date(self):
        if self.cleaned_data.get('birth_date') > datetime.date(datetime.today()):
            raise forms.ValidationError(
                self.error_messages['birthdate_isNotYet'],
                code='birthdate_isNotYet',
            )
        return self.data['birth_date']

    def clean_gender(self):
        if self.cleaned_data.get('gender') == '0':
            raise forms.ValidationError(
                self.error_messages['choise_gender'],
                code='choise_gender',
            )
        return self.data['gender']

    def clean_city(self):
        if self.cleaned_data.get('city') == '0':
            raise forms.ValidationError(
                self.error_messages['choise_city'],
                code='choise_city',
            )
        return self.data['city']

    def clean_university(self):
        if self.cleaned_data.get('university') == '0':
            raise forms.ValidationError(
                self.error_messages['choise_university'],
                code='choise_university',
            )
        return self.data['university']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if get_user_model().objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                self.error_messages['phone_exists'],
                code='phone_exists',
            )
        return phone

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        user.surname = self.cleaned_data['surname']
        user.name = self.cleaned_data['name']
        user.lastname = self.cleaned_data['lastname']

        user.city = self.cleaned_data['city']
        user.university = self.cleaned_data['university']
        user.faculty = self.cleaned_data['faculty']
        user.gender = self.cleaned_data['gender']
        user.birth_date = self.cleaned_data['birth_date']
        print(datetime.date(datetime.today()))
        # Получаем возраст пользователя из даты рождения с помощью деления на timedelta (при условии того, что каждый 4 год - високосный)
        age = (datetime.date(datetime.today()) - datetime.date(datetime.strptime(self.cleaned_data.get('birth_date'), '%Y-%m-%d'))) // timedelta(days=365.2425)
        user.age = age

        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']

        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()
        return user

# class AbstractAnalysisForm(ABC):

#     @abstractmethod
#     def get_form(self):
#         pass

#     class Meta: 
#         model = Parameter # ???? анализы или параметры??
#         fields = (
#              #????
#        )

# class OAKForm(AbstractAnalysisForm):
#     def get_form(self):
#         pass

DATE_INPUT_FORMATS = ['%Y-%m-%d',
                    '%m/%d/%Y',
                    '%m/%d/%y',
                    '%b %d %Y',
                    '%b %d, %Y',
                    '%d %b %Y',
                    '%d %b, %Y',
                    '%B %d %Y',
                    '%B %d, %Y',
                    '%d %B %Y',
                    '%d %B, %Y']

class OAKForm(forms.Form):
    date = forms.DateField(input_formats=DATE_INPUT_FORMATS, widget=forms.SelectDateWidget(years=YEARS, months=MONTHS), label='Дата анализа')

    gemoglobin = forms.FloatField(label='Гемоглобин')
    leycocite = forms.FloatField(label='Лейкоциты')
    eritrocity = forms.FloatField(label='Эритроциты')
    soe = forms.FloatField(label='СОЭ')

    def save(self, patient, commit=True):
        dateAnalysis = datetime.strptime(str(self.cleaned_data['date']), '%Y-%m-%d').strftime('%d/%m/%y')
        curr_analysis = Analysis(type='Общий Анализ Крови', time=self.cleaned_data['date'], patient=patient)

        p_gemoglobin = Parameter(name='Гемоглобин', result=self.cleaned_data['gemoglobin'], analysis=curr_analysis)
        p_leycocite = Parameter(name='Лейкоциты', result=self.cleaned_data['leycocite'], analysis=curr_analysis)
        p_eritrocity = Parameter(name='Эритроциты', result=self.cleaned_data['eritrocity'], analysis=curr_analysis)
        p_soe = Parameter(name='СОЭ', result=self.cleaned_data['soe'], analysis=curr_analysis)

        if commit:
            curr_analysis.save()

            p_gemoglobin.save()
            p_leycocite.save()
            p_eritrocity.save()
            p_soe.save()

class MeasurementForm(forms.Form):
    date = forms.DateField(input_formats=DATE_INPUT_FORMATS, widget=forms.SelectDateWidget(years=YEARS, months=MONTHS,), label='Дата измерений')

    sad = forms.FloatField(label='САД (Систолическое артериальное давление)')
    dad = forms.FloatField(label='ДАД (Диастолическое артериальное давление)')
    chss = forms.FloatField(label='ЧСС (Число сердечных сокращений)')
    chdd = forms.FloatField(label='ЧДД (Число дыхательных движений)')

    def save(self, patient, commit=True):
        dateAnalysis = datetime.strptime(str(self.cleaned_data['date']), '%Y-%m-%d').strftime('%d/%m/%y')
        curr_analysis = Analysis(type='Данные измерений', time=self.cleaned_data['date'], patient=patient)
        #print(f"Date anala: {dateAnalysis}")
        p_sad = Parameter(name='САД', result=self.cleaned_data['sad'], analysis=curr_analysis)
        p_dad  = Parameter(name='ДАД', result=self.cleaned_data['dad'], analysis=curr_analysis)
        p_chss = Parameter(name='ЧСС', result=self.cleaned_data['chss'], analysis=curr_analysis)
        p_chdd = Parameter(name='ЧДД', result=self.cleaned_data['chdd'], analysis=curr_analysis)

        if commit:
            curr_analysis.save()

            p_sad.save()
            p_dad.save()
            p_chss.save()
            p_chdd.save()

class CardiovisorForm(forms.Form):
    date = forms.DateField(input_formats=DATE_INPUT_FORMATS, widget=forms.SelectDateWidget(years=YEARS, months=MONTHS), label='Дата измерений')

    mio_index = forms.FloatField(label='Индекс миокарда')
    g1 = forms.FloatField(label='G1')
    g2 = forms.FloatField(label='G2')
    g3 = forms.FloatField(label='G3')

    def save(self, patient, commit=True):
        curr_analysis = Analysis(type='Данные кардиовизора', time=self.cleaned_data['date'], patient=patient)

        p_mio_index = Parameter(name='Индекс миокарда', result=self.cleaned_data['mio_index'], analysis=curr_analysis)
        p_g1 = Parameter(name='G1', result=self.cleaned_data['g1'], analysis=curr_analysis)
        p_g2 = Parameter(name='G2', result=self.cleaned_data['g2'], analysis=curr_analysis)
        p_g3 = Parameter(name='G3', result=self.cleaned_data['g3'], analysis=curr_analysis)

        if commit:
            curr_analysis.save()

            p_mio_index.save()
            p_g1.save()
            p_g2.save()
            p_g3.save()
