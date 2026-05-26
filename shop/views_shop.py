from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product
from .cart import Cart


def home(request):
    """Головна сторінка з описом магазину"""
    return render(request, 'shop/home.html')


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Фільтр за категорією
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Фільтр за категорією з GET-параметра
    cat_filter = request.GET.get('category')
    if cat_filter:
        products = products.filter(category__slug=cat_filter)
    
    # Фільтр за ціною
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    
    # Фільтр за розміром
    size = request.GET.get('size')
    if size:
        products = products.filter(description__icontains=size)
    
    # Пошук за назвою
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    
    # Сортування
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    else:
        products = products.order_by('-created')
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'selected_category': cat_filter or category_slug,
        'price_min': price_min,
        'price_max': price_max,
        'selected_size': size,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'shop/product_list.html', context)


def product_detail(request, id):  # тепер id замість product_slug
    """Детальна сторінка товару"""
    product = get_object_or_404(Product, id=id, available=True)
    
    # Схожі товари (з тієї ж категорії)
    similar_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    
    return render(request, 'shop/product_detail.html', context)

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    
    # Отримуємо кількість з POST запиту
    quantity = int(request.POST.get('quantity', 1))
    
    # Перевірка, щоб кількість не перевищувала залишок на складі
    if quantity > product.stock:
        quantity = product.stock
        messages.warning(request, f'Доступно лише {product.stock} шт. товару "{product.name}"')
    
    if quantity <= 0:
        quantity = 1
    
    # ОНОВЛЮЄМО кількість, а не додаємо
    cart.update(product=product, quantity=quantity)
    
    # Повертаємося на ту ж сторінку
    next_url = request.POST.get('next', 'shop:cart_detail')
    return redirect(next_url)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_count(request):
    cart = Cart(request)
    return JsonResponse({'count': cart.__len__()})


# Аутентифікація
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
    return redirect('shop:home')


@login_required
def profile(request):
    return render(request, 'shop/profile.html', {'user': request.user})

def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Фільтр за категорією
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Фільтр за категорією з GET-параметра
    cat_filter = request.GET.get('category')
    if cat_filter and cat_filter != '':
        products = products.filter(category__slug=cat_filter)
    
    # Фільтр за ціною (з перевіркою та конвертацією в число)
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    try:
        if price_min and price_min != '':
            price_min = float(price_min)
            if price_min < 0:
                price_min = 0
            products = products.filter(price__gte=price_min)
    except (ValueError, TypeError):
        price_min = ''
    
    try:
        if price_max and price_max != '':
            price_max = float(price_max)
            if price_max < 0:
                price_max = 0
            products = products.filter(price__lte=price_max)
    except (ValueError, TypeError):
        price_max = ''
    
    # Фільтр за розміром
    size = request.GET.get('size')
    if size and size != '':
        products = products.filter(description__icontains=size)
    
    # Пошук за назвою
    search_query = request.GET.get('search')
    if search_query and search_query != '':
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    
    # Сортування (ВАЖЛИВО: сортування за числом, а не рядком)
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        products = products.order_by('price')  # price - це DecimalField, сортується правильно
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    else:
        products = products.order_by('-created')
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'selected_category': cat_filter or category_slug,
        'price_min': price_min if price_min != '' else '',
        'price_max': price_max if price_max != '' else '',
        'selected_size': size,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'shop/product_list.html', context)

from .models import Review

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, 'Дякуємо за ваш відгук!')
        else:
            messages.error(request, 'Будь ласка, заповніть всі поля')
    
    return redirect('shop:product_detail', id=product_id)