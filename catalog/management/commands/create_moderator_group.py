from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу Модератор продуктов и назначает ей права'

    def handle(self, *args, **options):
        # Создаем или получаем группу
        moderator_group, created = Group.objects.get_or_create(
            name='Модератор продуктов')

        # Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Ищем кастомное право на отмену публикации и стандартное право на удаление продукта
        try:
            perm_unpublish = Permission.objects.get(
                codename='can_unpublish_product', content_type=content_type)
            perm_delete = Permission.objects.get(codename='delete_product',
                                                 content_type=content_type)

            # Добавляем права в группу
            moderator_group.permissions.add(perm_unpublish, perm_delete)

            self.stdout.write(self.style.SUCCESS(
                'Группа "Модератор продуктов" успешно создана и настроена!'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Ошибки при поиске прав. Сначала запустите миграции!'))
