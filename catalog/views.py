from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from django.views.generic import TemplateView

from catalog.forms import ProductForm
from catalog.models import Category
from catalog.models import Product
from catalog.services import get_products_by_category


class ProductListView(ListView):
    """Главная страница со списком товаров"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Если пользователь — модератор с правом отмены публикации, он видит абсолютно всё
        if user.is_authenticated and user.has_perm(
                'catalog.can_unpublish_product'):
            return queryset

        # Если пользователь авторизован, но он обычный клиент, он видит опубликованные товары + свои собственные
        if user.is_authenticated:
            return queryset.filter(Q(is_published=True) | Q(owner=user))

        # Анонимные пользователи видят исключительно опубликованные товары
        return queryset.filter(is_published=True)


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Доступ только авторизованным"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        # Автоматически привязываем текущего авторизованного пользователя к owner
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        # Продукт может изменить только пользователь, который его создал, или модератор.
        is_owner = self.object.owner == self.request.user
        is_moderator = self.request.user.has_perm('catalog.can_unpublish_product')

        if not (is_owner or is_moderator):
            raise PermissionDenied("Вы не можете редактировать этот продукт!")

        return self.object

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})



class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        # Удалять продукты должен не только владелец, но и модератор.
        # Проверяем, является ли пользователь владельцем ИЛИ имеет ли он право на удаление
        is_owner = self.object.owner == self.request.user
        is_moderator = self.request.user.has_perm('catalog.delete_product')

        if not (is_owner or is_moderator):
            raise PermissionDenied(
                "У вас нет прав на удаление этого продукта!")

        return self.object


class TogglePublishView(View):
    """Контроллер для быстрой смены статуса публикации модератором"""

    def post(self, request, pk):
        # Проверяем наличие кастомного права
        if not request.user.has_perm('catalog.can_unpublish_product'):
            raise PermissionDenied("У вас нет прав на управление публикацией!")

        product = Product.objects.get(pk=pk)
        # Переключаем статус на противоположный
        product.is_published = not product.is_published
        product.save()
        return redirect('catalog:product_detail', pk=pk)

class ContactsView(TemplateView):
    """Страница контактов"""
    template_name = 'catalog/contacts.html'


class CategoryProductListView(TemplateView):
    """Представление для вывода продуктов конкретной категории через сервисный слой"""
    template_name = 'catalog/category_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')

        # Получаем саму категорию для заголовка на странице
        context['category'] = Category.objects.get(pk=category_id)

        # View использует сервис для получения закэшированных данных
        context['products'] = get_products_by_category(category_id)
        return context
