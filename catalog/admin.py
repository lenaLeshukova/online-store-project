from django.contrib import admin
from catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Выводим id и name в списке категорий
    list_display = ('id', 'name')
    # Добавляем поиск по имени и описанию категории
    search_fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Выводим id, name, price и category в списке продуктов
    list_display = ('id', 'name', 'price', 'category')
    # Настраиваем фильтрацию продуктов по категории
    list_filter = ('category',)
    # Настраиваем поиск по полям name и description
    search_fields = ('name', 'description')
