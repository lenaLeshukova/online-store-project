from django.db import models
from django.conf import settings  # для AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Наименование'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True,
                              verbose_name='Изображение')
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата последнего изменения')

    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        # При удалении пользователя продукт не удалится, а останется без владельца
        blank=True,
        null=True,
        verbose_name='Владелец'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']
        # КАСТОМНЫЕ ПРАВА
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]

    def __str__(self):
        return self.name


# Модель для сохранения сообщений из формы обратной связи
class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения')

    def __str__(self):
        return f"Сообщение от {self.name} ({self.created_at})"
