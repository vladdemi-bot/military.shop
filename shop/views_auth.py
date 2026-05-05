from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST.get('email', '')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Користувач з таким іменем вже існує')
            return redirect('register')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, 'Реєстрація успішна! Тепер ви можете увійти')
        return redirect('login')
    
    return render(request, 'shop/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Вітаємо, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Невірне ім\'я користувача або пароль')
    
    return render(request, 'shop/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, 'Ви вийшли з системи')
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'shop/profile.html', {
        'user': request.user
    })