from django.core.management import call_command
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Очищает БД и загружает данные из фикстур'

    def handle(self, *args, **options):
        # 1. Предварительное удаление данных
        self.stdout.write(self.style.WARNING('Очистка старых данных...'))
        Product.objects.all().delete()
        Category.objects.all().delete()

        # 2. Загрузка данных из фикстур с выстраиванием связей
        self.stdout.write('Загрузка категорий и продуктов из фикстур...')
        try:
            # Сначала загружаем категории, затем продукты
            call_command('loaddata', 'category_data.json')
            call_command('loaddata', 'product_data.json')
            self.stdout.write(self.style.SUCCESS('База данных успешно заполнена из фикстур!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке фикстур: {e}'))
