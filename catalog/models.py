from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    """Категории товаров"""
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """Продукт"""
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    image = models.ImageField(**NULLABLE, upload_to='catalog/photo', verbose_name='Изображение',
                              help_text='Выберите изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='Дата изменения')
    viewed = models.IntegerField(default=0, verbose_name='Количество просмотров')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    slug = models.SlugField(**NULLABLE, max_length=150, unique=True, verbose_name="slug")

    owner = models.ForeignKey(User, verbose_name='Владелец', help_text='укажите владельца продукта', **NULLABLE,
                              on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name}, цена - {self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Version(models.Model):
    """Версия продукта"""
    name = models.CharField(max_length=150, verbose_name='Наименование')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='versions')
    version_number = models.PositiveIntegerField(verbose_name='Номер версии')
    is_actual = models.BooleanField(default=True, verbose_name='Актуальная')

    def __str__(self):
        return f'{self.name}, версия - {self.version_number}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ['product', 'version_number']
