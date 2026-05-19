from django.urls import path
from . import views_shop
from . import views_auth

app_name = 'shop'

urlpatterns = [
    path('', views_shop.home, name='home'),
    path('products/', views_shop.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views_shop.product_list, name='category_detail'),
    path('product/<int:id>/', views_shop.product_detail, name='product_detail'),  # ЗМІНИВ: тепер id замість slug
    path('cart/', views_shop.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views_shop.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views_shop.cart_remove, name='cart_remove'),
    path('cart/count/', views_shop.cart_count, name='cart_count'),
    path('register/', views_auth.register, name='register'),
    path('login/', views_auth.user_login, name='login'),
    path('logout/', views_auth.user_logout, name='logout'),
    path('profile/', views_auth.profile, name='profile'),
    path('review/add/<int:product_id>/', views_shop.add_review, name='add_review'),
]