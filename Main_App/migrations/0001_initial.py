# Generated by Django 3.2.7 on 2022-02-18 09:20

import Main_App.managers
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('surname', models.CharField(default='Christ', max_length=320, verbose_name='Фамилия')),
                ('name', models.CharField(default='Jesus', max_length=320, verbose_name='Имя')),
                ('lastname', models.CharField(blank=True, default=None, max_length=320, null=True, verbose_name='Отчество')),
                ('phone', models.CharField(blank=True, max_length=16, null=True, verbose_name='Phone')),
                ('city', models.CharField(blank=True, default='Voronezh', max_length=320, null=True, verbose_name='Город')),
                ('university', models.CharField(blank=True, default='ВГТУ', max_length=320, null=True, verbose_name='Учебное заведение')),
                ('faculty', models.CharField(blank=True, default='', max_length=320, null=True, verbose_name='Факультет')),
                ('gender', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Пол')),
                ('birth_date', models.DateTimeField(blank=True, default='2000-01-01 00:00:00', null=True, verbose_name='Дата рождения')),
                ('age', models.IntegerField(blank=True, default=1, null=True, verbose_name='Возраст')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Права администратора')),
                ('is_active', models.BooleanField(default=False, verbose_name='Учётная запись активна')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Права суперпользователя')),
                ('date_registration', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время регистрации')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время последнего входа в систему')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пациент',
                'verbose_name_plural': 'Пациенты',
            },
            managers=[
                ('objects', Main_App.managers.PatientManager()),
            ],
        ),
    ]
