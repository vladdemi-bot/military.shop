from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField('Назва', max_length=100)
    slug = models.SlugField(unique=True)
    # Видалено image поле

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_detail', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категорія')
    name = models.CharField('Назва товару', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Опис')
    price = models.DecimalField('Ціна (грн)', max_digits=10, decimal_places=2)
    old_price = models.DecimalField('Стара ціна', max_digits=10, decimal_places=2, blank=True, null=True)
    # Видалено image поле
    in_stock = models.BooleanField('В наявності', default=True)
    created_at = models.DateTimeField('Додано', auto_now_add=True)
    is_hit = models.BooleanField('Хіт продажу', default=False)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])
    
    def get_discount(self):
        if self.old_price:
            return int((1 - self.price / self.old_price) * 100)
        return 0