from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from django.forms import *

from .forms import *
from .models import *

import django.contrib.auth.models as mod

# Register your models here.

class Patient_Admin(UserAdmin):
    add_form = PatientCreationForm
    form = PatientChangeForm
    model = Patient

    # список юзеров в админке
    list_display = ('email', 'phone', 'surname', 'name', 'lastname', 'age', 'is_staff', 'is_active', 'is_superuser', )

    # фильтр в админке
    list_filter = ('is_staff', 'is_active', 'is_superuser', )

    # просмотр и изменение полей
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'surname', 'name', 'lastname', 'password', 'date_joined', 'date_registration', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', )}),
    )

    # поля при добавлении в админке
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'phone','surname', 'name', 'lastname', 'gender', 'birth_date', 'age','password1', 'password2', 'is_staff', 'is_active', 'is_superuser', )}
        ),
    )

    # поиск по полям
    search_fields = ('email', 'phone', 'surname', 'name', 'lastname',)

    # сортировка списка по полям
    ordering = ('email', 'phone', 'surname', 'name', 'lastname',)

admin.site.unregister(mod.Group)

admin.site.register(Patient, Patient_Admin)