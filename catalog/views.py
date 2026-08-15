from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView

from .forms import ContactForm, ProductForm
from .models import Product


class ProductListView(ListView):
    """Главная страница со списком товаров"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

class ProductDetailView(LoginRequiredMixin, DetailView):
    """Доступ только авторизованным"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ContactsView(CreateView):
    """Страница контактов с обработкой формы обратной связи"""
    form_class = ContactForm
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('catalog:contacts')


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Доступ только авторизованным"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Доступ только авторизованным"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Доступ только авторизованным"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
