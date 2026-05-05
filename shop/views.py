# Тимчасовий файл, щоб уникнути помилок
from django.shortcuts import render

def home(request):
    return render(request, 'shop/home.html')