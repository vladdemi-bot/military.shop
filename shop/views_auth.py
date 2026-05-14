from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Користувач з таким іменем вже існує')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Користувач з таким email вже існує')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Реєстрація пройшла успішно! Тепер увійдіть')
                return redirect('shop:login')
        else:
            messages.error(request, 'Паролі не співпадають')
    
    return render(request, 'shop/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Вітаємо, {username}! Ви увійшли в систему')
            return redirect('shop:product_list')
        else:
            messages.error(request, 'Невірне ім\'я користувача або пароль')
    
    return render(request, 'shop/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Ви вийшли з системи')
    return redirect('shop:product_list')


@login_required
def profile(request):
    return render(request, 'shop/profile.html', {'user': request.user})