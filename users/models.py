from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE, help_text='введите номер телефона')
    avatar = models.ImageField(upload_to='users/avatar', **NULLABLE, verbose_name='Аватар', help_text='выберите аватар')
    country = models.CharField(max_length=70, **NULLABLE, verbose_name='Страна', help_text='название страны')

    token = models.CharField(max_length=100, **NULLABLE, verbose_name='Token')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']

    def __str__(self):
        return f'{self.email}'
