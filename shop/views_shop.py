from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse  # ← ДОДАТИ ЦЕЙ РЯДОК!
from .models import Product, Category
from .cart import Cart

def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(in_stock=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Фільтр за ціною
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    categories = Category.objects.all()
    return render(request, 'shop/product_list.html', {
        'products': products,
        'category': category,
        'categories': categories,
    })

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, in_stock=True)
    return render(request, 'shop/product_detail.html', {'product': product})

@require_POST
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

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

def cart_count(request):
    """Повертає кількість товарів у кошику у форматі JSON"""
    cart = Cart(request)
    return JsonResponse({'count': len(cart)})