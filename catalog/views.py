from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Product
from catalog.forms import ContactForm


def home(request):
    # Использован лаконичный запрос
    products = Product.objects.all()
    # Контекст 'products' соответствует стилю 'books' в примере
    context = {'products': products}
    return render(request, 'catalog/home.html', context)


def product_detail(request, pk):
    # Контроллер получает pk, извлекает объект через ORM
    product = get_object_or_404(Product, pk=pk)
    # Контекст 'product' соответствует стилю 'book' в примере
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog:contacts')
    else:
        form = ContactForm()

    return render(request, 'catalog/contacts.html', {'form': form})
