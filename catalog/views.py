from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Product
from .forms import ContactForm


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
