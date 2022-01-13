# from django.db import models
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin

# from .managers import *

# from django.utils import timezone

# # Create your models here.

# #1
# class Patient(AbstractBaseUser, PermissionsMixin):
#     # required reg and auth field
#     email = models.EmailField(('Email'), unique=True)
#     phone = models.CharField(('Phone'), unique=True)

#     # personal info
#     surname = models.CharField(('Фамилия'), default="Christ", max_length=320)
#     name = models.CharField(('Имя'), default="Jesus", max_length=320)
#     lastname = models.CharField(('Отчество'), blank=True, null=True, default=None, max_length=320)

#     gender = models.CharField(('Пол'), blank=False, default=None, max_length=50)
#     birth_date = models.DateTimeField(('Дата рождения'), blank=False)
#     age = models.IntegerField(('Возраст'), blank=False)

#     date_registration = models.DateTimeField(('Дата и время регистрации'), default=timezone.now)
#     date_joined = models.DateTimeField(('Дата и время последнего входа в систему'), default=timezone.now)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = PatientManager()

#     def __str__(self) -> str:
#         return f"{self.surname} {self.name} {self.lastname}"

#     def get_full_name(self):
#         if self.lastname:
#             return f"{self.surname} {self.name} {self.lastname}"
#         return f"{self.surname} {self.name}"
    
#     class Meta:
#         verbose_name = ('Пациент')
#         verbose_name_plural = ('Пациенты')