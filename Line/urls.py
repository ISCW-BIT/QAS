from django.urls import path
from django.shortcuts import render
from django.conf.urls.static import static
from django.conf import settings

from .views import GetAnswer, Questions,LineAuthen,DisplayLineAuthen

app_name = 'Line'
urlpatterns = [
    path('<question_number>/Q',Questions, name = 'Question'),
    path('GA',GetAnswer, name = 'getanswer'),
    path('',Questions, name = 'Home'),
    path('liff',LineAuthen, name = 'liff'),
    path('auth',DisplayLineAuthen, name = 'auth'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)