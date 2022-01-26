from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='hello'),
    path('registration', views.registration, name='registration'),
    path('questionA', views.questionA, name='questionA'),
]