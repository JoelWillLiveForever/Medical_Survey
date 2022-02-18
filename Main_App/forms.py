from pyexpat import model
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date, timedelta
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from typing import Iterable

# from django.core.validators import validate_email
# from django.contrib.auth.password_validation import validate_password

from .models import *

class PatientCreationForm(UserCreationForm):

    class Meta:
        model = Patient
        fields = ('email', 'phone', 'surname', 'name', 'lastname', 'city', 'university', 'faculty', 'gender', 'birth_date', 'age', 'password')


class PatientChangeForm(UserChangeForm):

    class Meta:
        model = Patient
        fields = ('email', 'phone', 'surname', 'name', 'lastname', 'city', 'university', 'faculty', 'gender', 'birth_date', 'age', 'password')

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

    # def clean(self):
    #     email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(email=email, password=password)

    #     if not user or not user.is_active:
    #         raise forms.ValidationError(
    #             self.error_messages['not_user'],
    #             code='not_user',
    #         )
    #     return self.cleaned_data

    # def login(self, request):
    #     email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(email=email, password=password)
    #     return user
        
class RegistrationForm(UserCreationForm):

    surname = forms.CharField(required=True, label='* Фамилия', max_length=320, help_text='Не более 320 символов')
    name = forms.CharField(required=True, label='* Имя', max_length=320, help_text='Не более 320 символов')
    lastname = forms.CharField(required=False, label='* Отчество', max_length=320, help_text='Не более 320 символов')

    city = forms.CharField(required=False, label='* Город', max_length=320, help_text='Не более 320 символов')
    university = forms.CharField(required=False, label='* Университет', max_length=320, help_text='Используя сокращение прим. "ВГТУ"')
    faculty = forms.CharField(required=False, label='* Факультет', max_length=320, help_text='Используя сокращение прим. "ФИТКБ"')

    gender = forms.ChoiceField(required=True, label='* Пол', choices=[(1,'Мужской'), (2, 'Женский')], initial=1)

    MONTHS = {
    1:('Январь'), 2:('Февраль'), 3:('Март'), 4:('Апрель'),
    5:('Май'), 6:('Июнь'), 7:('Июль'), 8:('Август'),
    9:('Сентябрь'), 10:('Октябрь'), 11:('Ноябрь'), 12:('Декабрь')
    }
    YEARS = []
    for i in range(0, 2021-1920): #Заполнение селектора дат годами от 1922 до 2022
        YEARS.append(str((i-2022)*-1))
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=YEARS, months=MONTHS), label='* Дата рождения')

    email = forms.EmailField(required=True, label='* Адрес электронной почты', max_length=320, help_text='Не более 320 символов')

    phone = forms.CharField(required=True, label='* Номер телефона', max_length=18, help_text="Формат '+7' или '8'")

    password1 = forms.CharField(required=True, label='* Пароль', max_length=320, widget=forms.PasswordInput, help_text='Не менее 8 символов, цифры и верхний регистр')
    password2 = forms.CharField(required=True, label='* Повторите пароль', max_length=320, widget=forms.PasswordInput, help_text='Не менее 8 символов, цифры и верхний регистр')

    error_messages = {
        'email_exists': 'Пользователь с таким Email уже существует!',
        # 'email_not_valid': 'Некорректный Email-адрес!',
        # 'password_not_valid': 'Некорректный пароль!',
        'password_mismatch': 'Пароли не совпадают!',
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

        # Получаем возраст пользователя из даты рождения с помощью деления на timedelta (при условии того, что каждый 4 год - високосный)
        age = (date.today() - self.cleaned_data['birth_date']) // timedelta(days=365.2425)
        user.age = age

        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']

        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()
        return user