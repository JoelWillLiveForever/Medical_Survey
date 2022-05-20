from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='hello'),
    path('registration', views.registration, name='registration'),
    path('acc_active_sent', views.acc_active_sent, name='acc_active_sent'),
    path('acc_active_confirmed', views.acc_active_confirmed, name='acc_active_confirmed'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('login_page', views.login_page, name='login_page'),
    path('profile', views.profile, name='profile'),
    path('add_new_analysis', views.add_new_analysis, name='add_new_analysis'),
    path('question', views.question, name='question'),
]