from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ContactForm, ProductForm


class ProductListView(ListView):
    """Главная страница со списком товаров"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    """Страница детального просмотра товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ContactsView(CreateView):
    """Страница контактов с обработкой формы обратной связи"""
    form_class = ContactForm
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('catalog:contacts')


class ProductCreateView(CreateView):
    """Создание нового продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(UpdateView):
    """Редактирование существующего продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        """Перенаправление на страницу отредактированного товара"""
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    """Удаление продукта"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
