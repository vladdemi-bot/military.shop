from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Category, Product
from .cart import Cart


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    cart = Cart(request)
    cart_items = cart.cart.values()
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'cart_items': cart_items,
    })


@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('shop:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_count(request):
    cart = Cart(request)
    return JsonResponse({'count': len(cart)})


# ========== НОВІ ФУНКЦІЇ ДЛЯ РЕЄСТРАЦІЇ ==========

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