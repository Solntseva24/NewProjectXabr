from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('read_profile/', authapp.read_profile, name='read_profile'),
    path('edit/', authapp.edit, name='edit'),
    path('verify/<str:email>/<str:activation_key>/', authapp.verify, name='verify'),
    path('send/mail/confirm/', TemplateView.as_view(template_name='authapp/send_confirm.html'), name='send_confirm'),
]
