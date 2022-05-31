from django.urls import path
from django.shortcuts import render
from django.conf.urls.static import static
from django.conf import settings

from .views import RTAFLoginPage,RTAFLogin,Register


app_name = 'User'
urlpatterns = [
    path('',RTAFLoginPage,name = "rtaf-login"),
    path('auth',RTAFLogin,name = "authentication"),
    path('register',Register,name = "register"),

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)