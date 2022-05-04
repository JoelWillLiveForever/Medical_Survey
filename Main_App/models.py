from enum import Enum, unique
from tkinter import CASCADE
from xmlrpc.client import MAXINT
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.forms import CharField, ChoiceField

from .managers import *

from django.utils import timezone
from datetime import date

# Create your models here.

#1
class Patient(AbstractBaseUser, PermissionsMixin):
    # required reg and auth field
    email = models.EmailField(('Email'), unique=True)

    # personal info
    surname = models.CharField(('Фамилия'), default="Christ", max_length=320)
    name = models.CharField(('Имя'), default="Jesus", max_length=320)
    lastname = models.CharField(('Отчество'), blank=True, null=True, default=None, max_length=320)
    phone = models.CharField(('Телефон'), blank=True, null=True, max_length=16)

    # affiliation info
    city = models.CharField(('Город'), blank=True, null=True, default = 'Воронеж', max_length=320)
    university = models.CharField(('Учебное заведение'), blank=True, null=True, default= 'ВГТУ', max_length=320)
    faculty = models.CharField(('Факультет'), blank=True, null=True, default='', max_length=320)

    # physical info
    gender = models.CharField(('Пол'), blank=True, null=True, default='', max_length=50)
    birth_date = models.DateTimeField(('Дата рождения'), blank=True, null=True, default='2000-01-01 00:00:00')
    height = models.FloatField(('Рост'), blank=True, null=True, default=0)
    weight = models.FloatField(('Вес'), blank=True, null=True, default=0)

    # это поле не трогать, господь будет рад :)
    age = models.IntegerField(('Возраст'), blank=True, null=True, default=1)

    # permissions
    is_staff = models.BooleanField(('Права администратора'), default=False)
    is_active = models.BooleanField(('Учётная запись активна'), default=False)
    is_superuser = models.BooleanField(('Права суперпользователя'), default=False)

    date_registration = models.DateTimeField(('Дата и время регистрации'), default=timezone.now)
    date_joined = models.DateTimeField(('Дата и время последнего входа в систему'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = PatientManager()

    def __str__(self) -> str:
        return f"{self.surname} {self.name} {self.lastname}"

    def get_full_name(self):
        if self.lastname:
            return f"{self.surname} {self.name} {self.lastname}"
        return f"{self.surname} {self.name}"
    
    class Meta:
        verbose_name = ('Пациент')
        verbose_name_plural = ('Пациенты')

class Analysis(models.Model):
    type = models.CharField(max_length=150)
    time = models.DateTimeField(default=date.today())
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return '\n\tДата и Время: ' + str(self.time) + '\n\tТип: ' + self.type + '\n\tПациент: ' + str(self.patient)

class Parameter(models.Model):
    name = models.CharField(max_length=150)
    result = models.CharField(max_length=150)
    units = models.CharField(max_length=75)
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)

    def __str__(self):
        return '\n\tНазвание: ' + self.name + '\n\tРезультат: ' + self.result + '\n\tАнализ: ' + str(self.analysis)

class Block(models.Model):
    name = models.CharField(max_length=150, unique=True)

class Question(models.Model):
    TYPE_EASY = 'TE'
    TYPE_UNLOCK_CURRENT_BLOCK = 'TUCB'
    TYPE_UNLOCK_OTHER_BLOCK = 'TUOB'

    question = models.CharField(max_length=MAXINT, unique=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='block')
    
    CHOICES = [(TYPE_EASY, 'Easy'), (TYPE_UNLOCK_CURRENT_BLOCK, 'Unlock current block'), (TYPE_UNLOCK_OTHER_BLOCK, 'Unlock other block')]
    type = models.CharField(max_length=4, choices=CHOICES, default=TYPE_EASY)

    unlocked_block_code = models.ForeignKey(Block, blank=True, null=True, on_delete=models.CASCADE, related_name='unlocked_block', default=None)    

class Answer(models.Model):
    answer = models.BooleanField()

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

