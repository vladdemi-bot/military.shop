from django.shortcuts import render

def home(request):
    return render(request, 'shop/home.html')

from django.shortcuts import render

def home(request):
    return render(request, 'shop/home.html')

def about(request):
    return render(request, 'shop/about.html')

from django.urls import path
from .views import home, about

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
]




