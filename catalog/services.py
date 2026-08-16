from django.core.cache import cache
from django.conf import settings
from catalog.models import Product


def get_products_by_category(category_id):
    """
    Сервисная функция, возвращающая список опубликованных продуктов
    в указанной категории с использованием низкоуровневого кэширования.
    """
    # Ключ category_{id}
    cache_key = f'category_{category_id}'

    # Пытаемся получить данные из кэша Redis
    products = cache.get(cache_key)

    # Если данных в кэше нет — берем их из базы данных и сохраняем в Redis
    if products is None:
        # Фильтруем продукты по категории и статусу публикации
        products = list(
            Product.objects.filter(category_id=category_id, is_published=True))

        # Задаем TTL (время жизни кэша из settings) и сохраняем по ключу
        cache.add(cache_key, products, timeout=settings.CACHE_TTL)

    return products
